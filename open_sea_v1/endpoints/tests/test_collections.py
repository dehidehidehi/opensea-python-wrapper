from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.collections import CollectionsEndpoint
from open_sea_v1.helpers.testing_class import QueryTestCase


class TestCollectionsEndpoint(QueryTestCase):

    endpoint = CollectionsEndpoint

    def setUp(self) -> None:
        self.endpoint_kwargs = dict(
            client_params=ClientParams(limit=2, max_pages=1, page_size=2),
        )
        self.asset_owner = '0xd387a6e4e84a6c86bd90c158c6028a58cc8ac459'  # pranksy

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
