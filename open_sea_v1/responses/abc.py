from abc import ABC


class BaseResponse(ABC):
    """Parent class for OpenSea API Responses."""

    def __init__(self, _json: dict = None):
        self._json = _json
