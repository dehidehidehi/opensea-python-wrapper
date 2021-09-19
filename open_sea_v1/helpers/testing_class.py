from abc import ABC, abstractmethod
from itertools import chain
from typing import Type
from unittest import TestCase

from open_sea_v1.endpoints.abc import BaseEndpoint
from open_sea_v1.responses.abc import BaseResponse


class QueryTestCase(TestCase, ABC):

    sample_wallet = "0x5ca12f79e4d33b0bd153b40df59f6db9ee03482e"  # punk
    sample_contract = "0x76be3b62873462d2142405439777e971754e8e77"
    token_ids = [10137, 10089, 87]

    @property
    @abstractmethod
    def endpoint(self) -> Type[BaseEndpoint]:
        """"""

    def create_and_get(self, **kwargs) -> list[BaseResponse]:
        """Shortcut"""
        client = self.endpoint(**kwargs)  # type: ignore
        flattened = client.get_parsed_pages(flat=True)
        return flattened