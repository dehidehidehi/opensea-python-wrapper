from abc import ABC
from dataclasses import dataclass
from typing import Optional, Generator

from requests import Response, request

from open_sea_v1.responses import OpenSeaAPIResponse

@dataclass
class _ClientParams:
    """Common OpenSea Endpoint parameters to pass in."""
    offset: int = 0
    limit: int = 20
    max_pages: Optional[int] = None
    api_key: Optional[str] = None


class BaseOpenSeaClient(ABC):
    client_params: _ClientParams
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

    def get_pages(self) -> Generator[list[list[OpenSeaAPIResponse]], None, None]:
        self._http_response = None
        while self.remaining_pages():
            self._http_response = self._get_request()
            yield self.parsed_http_response
            self.client_params.offset += self.client_params.limit
            self.processed_pages += 1

    def remaining_pages(self) -> bool:
        if self._http_response is None:
            return True
        if self.client_params.max_pages is not None and self.processed_pages <= self.client_params.max_pages:
            return True
        if len(self.response) >= self.client_params.offset:
            return True
        return False
