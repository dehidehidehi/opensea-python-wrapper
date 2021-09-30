from typing import Type
from unittest import TestCase

from open_sea_v1.endpoints.abc import BaseEndpoint
from open_sea_v1.responses.abc import BaseResponse


class ResponseTestHelper(TestCase):

    @classmethod
    def create_and_get(cls, endpoint_client: Type[BaseEndpoint],  **kwargs) -> list[list[BaseResponse]]:
        """Shortcut"""
        client = endpoint_client(**kwargs)  # type: ignore
        flattened = client.get_parsed_pages(flat=True)
        return flattened

    @staticmethod
    def assert_attributes_do_not_raise_unexpected_exceptions(target_obj):
        attrs = [n for n in dir(target_obj) if not n.startswith('__')]
        for a in attrs:
            getattr(target_obj, a)

    @staticmethod
    def assert_no_missing_class_attributes_from_original_json_keys(response_obj, json):
        for key in json:
            getattr(response_obj, key)
