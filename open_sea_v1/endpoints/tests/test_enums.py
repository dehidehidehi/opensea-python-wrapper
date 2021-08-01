from unittest import TestCase

import requests

from open_sea_v1.endpoints.endpoint_enums import OpenseaApiEndpoints, ExtendedStrEnum


class TestExtendedStrEnum(TestCase):

    def test_extended_str_enum_class_method_list_values_returns_all_values(self):
        class TestEnum(ExtendedStrEnum):
            VALUE_1 = "value_1"
            VALUE_2 = "value_2"
        self.assertTrue(TestEnum.list(), ["value_1", "value_2"])


class TestAPIEndpoints(TestCase):

    def test_endpoints_urls_responds_with_a_json(self):
        for url in OpenseaApiEndpoints:
            resp = requests.get(url.value).json()
            self.assertTrue(resp, f"JSON Reponse was empty for {resp}")
