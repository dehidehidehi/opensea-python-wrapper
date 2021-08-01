from unittest import TestCase

from open_sea_v1.endpoints import AssetsEndpoint
from open_sea_v1.responses import AssetResponse


class TestAssetObj(TestCase):
    sample_contract = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"  # punk
    default_asset_params = dict(token_ids=[5, 6, 7], asset_contract_address=sample_contract)

    @classmethod
    def setUpClass(cls) -> None:
        params = cls.default_asset_params | dict(token_ids=[1, 14, 33])
        cls.assets = cls.create_and_get(**params)

    @classmethod
    def create_and_get(cls, **kwargs) -> list[AssetResponse]:
        """Shortcut"""
        client = AssetsEndpoint(**kwargs)
        client.get_request()
        return client.response

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        target_obj = self.assets[0]
        attrs = [n for n in dir(target_obj) if not n.startswith('__')]
        for a in attrs:
            getattr(target_obj, a)


