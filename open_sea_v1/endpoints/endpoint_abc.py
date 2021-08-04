from abc import ABC, abstractmethod
from typing import Optional, Union, Generator

from requests import Response

from open_sea_v1.endpoints.endpoint_client import _ClientParams
from open_sea_v1.responses.response_abc import _OpenSeaResponse


class BaseOpenSeaEndpoint(ABC):

    @property
    @abstractmethod
    def __post_init__(self):
        """Using post_init to run param validation"""

    @property
    @abstractmethod
    def client_params(self) -> _ClientParams:
        """Instance of common OpenSea Endpoint parameters."""

    @property
    @abstractmethod
    def url(self) -> str:
        """Endpoint URL"""

    @property
    @abstractmethod
    def get_pages(self) -> Generator[list[list[_OpenSeaResponse]], None, None]:
        """Returns all pages for the query."""

    @property
    @abstractmethod
    def parsed_http_response(self) -> Union[list[_OpenSeaResponse], _OpenSeaResponse]:
        """Parsed JSON dictionnary from HTTP Response."""

    @abstractmethod
    def _get_request(self) -> Response:
        """Returns HTTP parsed_http_response from OpenSea."""

    @property
    @abstractmethod
    def _validate_request_params(self) -> None:
        """"""
