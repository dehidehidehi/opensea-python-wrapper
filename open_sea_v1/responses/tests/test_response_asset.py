from open_sea_v1.endpoints import AssetsEndpoint
from open_sea_v1.responses.tests._response_helpers import ResponseTestHelper


class TestAssetObj(ResponseTestHelper):
    sample_contract = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"  # punk
    default_asset_params = dict(token_ids=[5, 6, 7], asset_contract_address=sample_contract)

    @classmethod
    def setUpClass(cls) -> None:
        params = cls.default_asset_params | dict(token_ids=[1, 14, 33])
        cls.assets = cls.create_and_get(AssetsEndpoint, **params)
        cls.asset = cls.assets[0]

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        self.assert_attributes_do_not_raise_unexpected_exceptions(self.asset)

    def test_no_missing_class_attributes_from_original_json_keys(self):
        self.assert_no_missing_class_attributes_from_original_json_keys(response_obj=self.asset, json=self.asset._json)

