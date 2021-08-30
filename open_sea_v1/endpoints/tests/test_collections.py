from unittest import TestCase

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.collections import CollectionsEndpoint
from open_sea_v1.responses.collection import CollectionResponse


class TestCollectionsEndpoint(TestCase):

    def setUp(self) -> None:
        self.asset_owner = "0x5ca12f79e4d33b0bd153b40df59f6db9ee03482e"  # punk
        self.endpoint_kwargs = dict(
            client_params=ClientParams(limit=2, max_pages=1, page_size=2),
        )

    @staticmethod
    def create_and_get(**kwargs) -> list[CollectionResponse]:
        collections_client = CollectionsEndpoint(**kwargs)
        collections_client._get_request()
        return collections_client.parsed_http_response

    def test_collection_resp_works(self):
        basic_collections_resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(basic_collections_resp)

        self.endpoint_kwargs |= dict(asset_owner=self.asset_owner)
        owner_asset_collections_resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(owner_asset_collections_resp)

        self.assertNotEqual(
            {c.slug for c in basic_collections_resp},
            {c.slug for c in owner_asset_collections_resp},
        )
