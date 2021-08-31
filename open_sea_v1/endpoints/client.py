import logging
from abc import ABC
from dataclasses import dataclass
from typing import Optional, Generator, Union

from ratelimit import limits, sleep_and_retry
from requests import Response, request

from open_sea_v1.responses.abc import BaseResponse

logger = logging.getLogger(__name__)

MAX_CALLS_PER_SECOND = 2  # gets overriden if API key is passed to ClientParams instance
RATE_LIMIT = 1  # second

@dataclass
class ClientParams:
    """Common OpenSea Endpoint parameters to pass in."""
    offset: int = 0
    page_size: int = 50
    limit: Optional[int] = None
    max_pages: Optional[int] = None
    api_key: Optional[str] = None

    def __post_init__(self):
        self._validate_attrs()
        self._decrement_max_pages_attr()
        self._set_max_rate_limit()

    def _validate_attrs(self) -> None:
        if self.limit is not None and not 0 < self.limit <= 300:
            raise ValueError(f'{self.limit=} must be over 0 and lesser or equal to 300.')
        if self.page_size is not None and not 0 <= self.page_size <= 50:
            raise ValueError(f'{self.page_size=} must be between 0 and 50.')
        if self.max_pages is not None and self.max_pages < 0:
            raise ValueError(f'{self.max_pages=} must be greater than or equal to 0.')

    def _decrement_max_pages_attr(self) -> None:
        """
        For OpenSea, the max pages attribute starts at zero.
        However, and for clarity our package, will have this value start at 1 and decrement it for OpenSea.
        """
        if self.max_pages is not None:
            self.max_pages -= 1

    def _set_max_rate_limit(self) -> None:
        global MAX_CALLS_PER_SECOND
        MAX_CALLS_PER_SECOND = 2  # per second
        if self.api_key:
            raise NotImplementedError("I don't know what the rate limit is for calls with an API key is yet.")


class BaseClient(ABC):
    client_params: ClientParams
    processed_pages: int = 0
    response = None
    parsed_http_response = None
    url = None
    rate_limiting: bool = True
    _http_response = None
    _rate_limiting_timer: float = 0.0

    @property
    def http_headers(self) -> dict:
        params = {'headers': dict()}
        if self.client_params.api_key:
            params['headers'] = {'X-API-Key': self.client_params.api_key}
        return params

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_SECOND, period=RATE_LIMIT)
    def _get_request(self, **kwargs) -> Response:
        """Get requests with a rate limiter."""
        updated_kwargs = kwargs | self.http_headers
        return request('GET', self.url, **updated_kwargs)

    def get_pages(self) -> Generator[list[list[BaseResponse]], None, None]:
        self.processed_pages = 0
        self.client_params.offset = 0 if self.client_params.offset is None else self.client_params.offset
        self._http_response = None

        while self.remaining_pages():
            self._http_response = self._get_request()
            if self.parsed_http_response is not None:  # edge case
                self.processed_pages += 1
                self.client_params.offset += self.client_params.page_size
                yield self.parsed_http_response

    def remaining_pages(self) -> bool:
        if self._http_response is None:
            return True

        if (max_pages_was_set := self.client_params.max_pages is not None) and \
            (previous_page_was_not_empty := len(self.parsed_http_response) > 0) and \
                (remaining_pages_until_max_pages := self.processed_pages <= self.client_params.max_pages):
            return True

        if is_not_the_last_page := len(self.parsed_http_response) >= self.client_params.offset:
            return True
        return False
