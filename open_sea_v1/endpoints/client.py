import asyncio
import logging
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import chain
from os import environ
from typing import Optional, Type, Union

import ujson
from aiohttp import ClientSession
from requests.models import PreparedRequest

from open_sea_v1.helpers.rate_limiter import RateLimiter
from open_sea_v1.responses.abc import BaseResponse

logger = logging.getLogger(__name__)

@dataclass
class ClientParams:
    """
    Common OpenSea Endpoint parameters to pass in.
    Will automatically use OPENSEA_API_KEY environment variable as the api_key value, if it exists on the system.
    """
    offset: int = 0
    page_size: int = 50
    limit: int = 50
    max_pages: Optional[int] = None
    api_key: Optional[str] = None

    def __post_init__(self):
        # if self.max_pages:
        #     self.max_pages += 1  # prevent paginator from ending one page early
        self._attempt_setting_the_api_key()
        self._validate_attrs()

    def _validate_attrs(self) -> None:
        if not 0 < self.limit <= 300:
            raise ValueError(f'{self.limit=} must be over 0 and lesser or equal to 300.')

        if self.max_pages is not None and self.max_pages <= 0:
            raise ValueError(f'{self.max_pages=} must be greater than 0.')

        if not 0 <= self.page_size <= 50:
            raise ValueError(f'{self.page_size=} must be between 0 and 50.')

        if self.limit < self.page_size:
            raise ValueError(f'{self.limit=} cannot be lesser than {self.page_size=}.')

        if self.max_pages is not None and self.max_pages < 0:
            raise ValueError(f'{self.max_pages=} must be greater than or equal to 0.')

    def _decrement_max_pages_attr(self) -> None:
        """
        For OpenSea, the max pages attribute starts at zero.
        However, and for clarity our package, will have this value start at 1 and decrement it for OpenSea.
        """
        if self.max_pages is not None:
            self.max_pages -= 1

    def _attempt_setting_the_api_key(self) -> None:
        self.api_key = environ.get('OPENSEA_API_KEY')


@dataclass
class BaseClient(ABC):
    """
    This is a partial implementation of a client class.
    You cannot instanciate this.
    Because of this, you can, however, access the children classes attributes and properties.

    Parameters
    ----------
    client_params:
        ClientParams instance.

    _rate_limit: int
        Rate limit for the API is 20 when you have an API key.
        However, you run the risk of losing a a few seconds if you get throttled by the server.
        After some testing, it seems 18 is the sweet spot.

    _concurrency_limit: int
        Concurrency limit: number of simultaneous connections at a time.
        Best results obtained by using the largest multiple of _rate_limit, or second largest multiple.
        Otherwise you risk more throttling on the serverside than necessary.
    """

    client_params: ClientParams
    url = None

    _rate_limit: int = 18
    _concurrency_limit: int = 5

    def __post_init__(self):
        self.processed_pages: int = 0
        self.response = None
        self.parsed_http_response = None
        self._latest_json_response = None

        self._rate_limit = 2 if not self.client_params.api_key else self._rate_limit

    @property
    @abstractmethod
    def _json_resp_key(self) -> str:
        """To access the contents of a page from the contents of an OpenSea HTTP response,
         you need to use a dictionnary key."""

    @property
    def http_headers(self) -> dict:
        headers = dict()
        if self.client_params.api_key:
            headers['X-API-Key'] = self.client_params.api_key
        return headers

    def get_parsed_pages(self, flat: bool = True) -> list:
        """Wraps a call to _get_parsed_pages() in a try block to catch various network errors and log them."""
        from aiohttp.client_exceptions import ContentTypeError
        try:
            return self._get_parsed_pages(flat)
        except ContentTypeError as err:
            message = f'The request likely encountered a server side error.\n'\
                      f'So far this has happened when OpenSea requires a mandatory API key for certain endpoints.\n'\
                      f'Check https://twitter.com/apiopensea for endpoint status updates.\n'\
                      f'Error: {err.message}'
            logger.exception(message, exc_info=err)
            raise ConnectionError(message) from err

    def _get_parsed_pages(self, flat: bool = True) -> list:
        """Dispatches to the correct function depending on whether the user has an API key or not."""
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # prevents closed loops errors on windows
        self._latest_json_response = None  # reset: required for pagination function
        results = asyncio.run(self._aget_parsed_pages())
        if not flat:
            return results
        flattened = list(chain.from_iterable(results))
        return flattened

    async def _aget_parsed_pages(self) -> list[list[Type[BaseResponse]]]:
        all_parsed_jsons = list()

        async with RateLimiter(rate_limit=self._rate_limit, concurrency_limit=self._concurrency_limit) as rate_limiter:
            async with ClientSession(headers=self.http_headers, json_serialize=ujson.dumps) as session:
                json_batch = await self._async_get_pages_jsons(session, rate_limiter=rate_limiter)
                parsed_json_batch = [self._parse_json(j) for j in json_batch]
                all_parsed_jsons.extend(parsed_json_batch)

        return all_parsed_jsons

    async def _async_get_pages_jsons(self, session, *, rate_limiter: RateLimiter) -> Optional[list[dict]]:
        responses = list()
        processed_pages = 0
        while self._remaining_pages():

            self.client_params.offset += self.client_params.page_size
            params = {**self.get_params, **{'offset': self.client_params.offset}}  # type: ignore
            querystring = self.mk_querystring(self.url, params=params)

            async with rate_limiter.throttle():
                resp = await session.get(querystring)
                json_resp = await resp.json()
                self._latest_json_response = json_resp
                self.client_params._decrement_max_pages_attr()
                processed_pages += 1

            if potential_error_occurred := isinstance(json_resp, dict) and 'detail' in json_resp.keys():
                raise ConnectionError(f'{(error_msg := json_resp["detail"])}')

            logger.info(f'Fetched page #{processed_pages} (~{self.client_params.page_size} elements)')
            responses.append(json_resp)
        return responses

    def _parse_json(self, the_json: Union[dict, list]) -> list[Type[BaseResponse]]:
        if not the_json:
            return list()

        if isinstance(the_json, dict):
            json_list = the_json[self._json_resp_key]  # type: ignore

        if isinstance(the_json, list):
            flattened = list(chain.from_iterable(the_json)) if isinstance(the_json[0], list) else the_json  # just in case multiple pages
            json_list = list(chain.from_iterable(j.get(self._json_resp_key) or [j] for j in flattened))

        responses = [self._response_type(element) for element in json_list]  # type: ignore
        return responses

    def _remaining_pages(self) -> bool:
        if self._latest_json_response is None:
            return True
        if is_the_last_page := len(self._parse_json(self._latest_json_response)) < self.client_params.page_size:
            return False
        max_pages_reached: bool = self.client_params.max_pages is not None and self.client_params.max_pages <= 0
        if max_pages_reached:
            return False
        return True

    @staticmethod
    def mk_querystring(url, params) -> str:
        url_prepper = PreparedRequest()
        url_prepper.prepare_url(url, params)
        return url_prepper.url