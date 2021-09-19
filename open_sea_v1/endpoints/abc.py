from abc import ABC, abstractmethod
from typing import Generator, Type

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
    def _response_type(self) -> Type[BaseResponse]:
        """"""

    @property
    @abstractmethod
    def url(self) -> str:
        """Endpoint URL"""

    @abstractmethod
    def _parse_json(self) -> Generator[list[list[BaseResponse]], None, None]:
        """Returns all pages for the query."""

    @property
    @abstractmethod
    def get_params(self) -> str:
        """Endpoint URL"""

    @property
    @abstractmethod
    def _validate_request_params(self) -> None:
        """"""
