from unittest import TestCase

from open_sea_v1.responses.response_abc import _OpenSeaResponse


class ResponseTestHelper(TestCase):

    @classmethod
    def create_and_get(cls, endpoint_client,  **kwargs) -> list[_OpenSeaResponse]:
        """Shortcut"""
        client = endpoint_client(**kwargs)
        client._get_request()
        return client.parsed_http_response

    @staticmethod
    def assert_attributes_do_not_raise_unexpected_exceptions(target_obj):
        attrs = [n for n in dir(target_obj) if not n.startswith('__')]
        for a in attrs:
            getattr(target_obj, a)

    @staticmethod
    def assert_no_missing_class_attributes_from_original_json_keys(response_obj, json):
        for key in json:
            getattr(response_obj, key)
