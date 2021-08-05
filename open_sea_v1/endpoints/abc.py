from abc import ABC, abstractmethod
from typing import Optional, Union, Generator

from requests import Response

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.responses.abc import BaseResponse


class BaseEndpoint(ABC):

    @property
    @abstractmethod
    def __post_init__(self):
        """Using post_init to run param validation"""

    @property
    @abstractmethod
    def client_params(self) -> ClientParams:
        """Instance of common OpenSea Endpoint parameters."""

    @property
    @abstractmethod
    def url(self) -> str:
        """Endpoint URL"""

    @property
    @abstractmethod
    def parsed_http_response(self) -> Union[list[BaseResponse], BaseResponse]:
        """Parsed JSON dictionnary from HTTP Response."""

    @abstractmethod
    def _get_request(self) -> Response:
        """Returns HTTP parsed_http_response from OpenSea."""

    @property
    @abstractmethod
    def _validate_request_params(self) -> None:
        """"""

    @abstractmethod
    def get_pages(self) -> Generator[list[list[BaseResponse]], None, None]:
        """Returns all pages for the query."""
