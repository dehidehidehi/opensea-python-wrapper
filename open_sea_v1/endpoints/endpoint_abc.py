from abc import ABC, abstractmethod
from typing import Optional, Union

from requests import Response

from open_sea_v1.responses.response__base import _OpenSeaAPIResponse


class BaseOpenSeaEndpoint(ABC):

    @property
    @abstractmethod
    def __post_init__(self):
        """Using post_init to run param validation"""

    @property
    @abstractmethod
    def api_key(self) -> Optional[str]:
        """Optional OpenSea API key"""

    @property
    @abstractmethod
    def url(self) -> str:
        """Endpoint URL"""

    @property
    @abstractmethod
    def _request_params(self) -> dict:
        """Dictionnary of _request_params to pass into the _get_request."""

    @property
    @abstractmethod
    def _validate_request_params(self) -> None:
        """"""

    @property
    @abstractmethod
    def response(self) -> Union[list[_OpenSeaAPIResponse], _OpenSeaAPIResponse]:
        """Parsed JSON dictionnary from HTTP Response."""

    @property
    @abstractmethod
    def http_response(self) -> Optional[Response]:
        """HTTP Response from Opensea API."""

    @abstractmethod
    def get_request(self, url: str, method: str = 'GET', **kwargs) -> Response:
        """Call to super()._get_request passing url and _request_params."""

