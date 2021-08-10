from abc import ABC
from dataclasses import dataclass
from typing import Optional, Generator

from requests import Response, request

from open_sea_v1.responses.abc import BaseResponse

@dataclass
class ClientParams:
    """Common OpenSea Endpoint parameters to pass in."""
    offset: int = 0
    page_size: int = 50
    limit: Optional[int] = None
    max_pages: Optional[int] = None
    api_key: Optional[str] = None

    def __post_init__(self):
        if self.limit is not None and not 0 < int(self.limit) <= 300:
            raise ValueError(f'{self.limit=} max value is 300.')


class BaseClient(ABC):
    client_params: ClientParams
    processed_pages: int = 0
    response = None
    parsed_http_response = None
    url = None
    _http_response = None

    @property
    def http_headers(self) -> dict:
        params = {'headers': dict()}
        if self.client_params.api_key:
            params['headers'] = {'X-API-Key': self.client_params.api_key}
        return params

    def _get_request(self, **kwargs) -> Response:
        updated_kwargs = kwargs | self.http_headers
        return request('GET', self.url, **updated_kwargs)

    def get_pages(self) -> Generator[list[list[BaseResponse]], None, None]:
        self.processed_pages = 0
        self.client_params.offset = 0
        self._http_response = None

        while self.remaining_pages():
            self._http_response = self._get_request()
            if self.parsed_http_response:  # edge case
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
