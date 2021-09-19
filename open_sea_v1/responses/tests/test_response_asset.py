from open_sea_v1.endpoints.abc import ClientParams
from open_sea_v1.endpoints.assets import AssetsEndpoint
from open_sea_v1.responses.tests._response_helpers import ResponseTestHelper


class TestAssetObj(ResponseTestHelper):
    sample_contract = "0x76be3b62873462d2142405439777e971754e8e77"
    default_asset_params = dict(
        client_params=ClientParams(limit=1, page_size=1, max_pages=1),
        token_ids=[10137, 10089, 87],
        asset_contract_address=sample_contract
    )

    @classmethod
    def setUpClass(cls) -> None:
        params = cls.default_asset_params | dict(token_ids=[1, 14, 33])
        cls.assets = cls.create_and_get(AssetsEndpoint, **params)
        cls.asset = cls.assets[0]  # type: ignore

    def test_asset_property_is_not_empty(self):
        self.assertTrue(self.asset)

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        self.assert_attributes_do_not_raise_unexpected_exceptions(self.asset)

    def test_no_missing_class_attributes_from_original_json_keys(self):
        self.assert_no_missing_class_attributes_from_original_json_keys(response_obj=self.asset, json=self.asset._json)

