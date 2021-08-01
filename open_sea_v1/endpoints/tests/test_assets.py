from itertools import combinations
from unittest import TestCase

from open_sea_v1.endpoints.endpoint_assets import AssetsEndpoint
from open_sea_v1.endpoints.endpoint_enums import AssetsOrderBy
from open_sea_v1.responses.asset_obj import Asset


class TestAssetsRequest(TestCase):
    sample_contract = "0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb"  # punk
    sample_wallet = "0x5ca12f79e4d33b0bd153b40df59f6db9ee03482e"  # punk
    default_asset_params = dict(token_ids=[5, 6, 7], asset_contract_address=sample_contract)

    @staticmethod
    def create_and_get(**kwargs) -> list[Asset]:
        """Shortcut"""
        client = AssetsEndpoint(**kwargs)
        client.get_request()
        return client.response

    def test_cannot_all_be_none_owner_token_ids_asset_contract_address_asset_contract_addresses_collection(self):
        assets_kwargs = dict(owner=0, token_ids=0, collection=0, asset_contract_address=0, asset_contract_addresses=0)
        for kwarg_combo in combinations(assets_kwargs, r=len(assets_kwargs)):
            self.assertRaises(ValueError, AssetsEndpoint, kwarg_combo)

    def test_param_owner_returns_assets_from_specified_owner(self):
        params = dict(owner=self.sample_wallet, order_direction='asc', **self.default_asset_params)
        for punk in self.create_and_get(**params):
            self.assertEqual(punk.owner.address, self.sample_wallet)

    def test_param_token_ids_raise_exception_if_missing_contract_address_and_addresses(self):
        self.assertRaises(ValueError, AssetsEndpoint, token_ids=[1, 2, 3])

    def test_params_cannot_be_simultaneously_be_passed_asset_contract_address_and_contract_addresses(self):
        params = self.default_asset_params | dict(asset_contract_address=True, asset_contract_addresses=True)
        self.assertRaises(ValueError, AssetsEndpoint, **params)

    def test_param_token_ids_returns_assets_corresponding_to_single_contract(self):
        params = dict(order_direction='asc', **self.default_asset_params)
        for punk in self.create_and_get(**params):
            self.assertEqual(punk.asset_contract.address, self.sample_contract)

    def test_param_order_direction_can_only_be_asc_or_desc(self):
        invalid_order_values = (False, 0, 1, "", [], (), {}, 'hi')
        for invalid_order in invalid_order_values:
            params = dict(token_ids=[1], asset_contract_address=self.sample_contract, order_direction=invalid_order)
            self.assertRaises((ValueError, TypeError), AssetsEndpoint, **params)

    def test_param_order_by_token_id(self):
        params = self.default_asset_params | dict(token_ids=[3, 2, 1], order_by=AssetsOrderBy.TOKEN_ID, order_direction='desc')
        punks_ids = [punk.token_id for punk in self.create_and_get(**params)]
        self.assertEqual(['3', '2', '1'], punks_ids)

    def test_param_order_by_sale_date(self):
        params = self.default_asset_params | dict(token_ids=[1, 14, 33], order_by=AssetsOrderBy.SALE_DATE)
        punks_sales = [punk.last_sale.event_timestamp for punk in self.create_and_get(**params)]
        self.assertEqual(sorted(punks_sales, reverse=True), punks_sales)

    def test_param_order_by_sale_count(self):
        params = self.default_asset_params | dict(token_ids=[1, 14, 33], order_by=AssetsOrderBy.SALE_COUNT)
        punks_sales_cnt = [punk.num_sales for punk in self.create_and_get(**params)]
        self.assertEqual(sorted(punks_sales_cnt, reverse=True), punks_sales_cnt)

    def test_param_order_by_sale_price(self):
        params = self.default_asset_params | dict(token_ids=[1, 14, 33], order_by=AssetsOrderBy.SALE_PRICE)
        punks_last_sale_price = [punk.last_sale.total_price for punk in self.create_and_get(**params)]
        self.assertEqual(sorted(punks_last_sale_price, reverse=True), punks_last_sale_price)

    def test_param_order_by_visitor_count(self):
        pass  # as far as I know this is not returned in the API http_response and done directly by OpenSea

    def test_param_limit_cannot_be_below_0_or_above_50(self):
        self.assertRaises(ValueError, AssetsEndpoint, limit="25", **self.default_asset_params)
        self.assertRaises(ValueError, AssetsEndpoint, limit=-1, **self.default_asset_params)
        self.assertRaises(ValueError, AssetsEndpoint, limit=51, **self.default_asset_params)