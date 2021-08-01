from abc import ABC, abstractmethod
from typing import Optional

from requests import Response


class BaseOpenSeaEndpoint(ABC):

    @abstractmethod
    def get_request(self, url: str, method: str = 'GET', **kwargs) -> Response:
        """Call to super().get_request passing url and _request_params."""

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
        """Dictionnary of _request_params to pass into the get_request."""

    @property
    @abstractmethod
    def validate_request_params(self) -> None:
        """"""

    @property
    @abstractmethod
    def response(self) -> list[dict]:
        """Parsed JSON dictionnary from HTTP Response."""
