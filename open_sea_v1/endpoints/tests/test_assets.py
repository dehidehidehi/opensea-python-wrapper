from itertools import combinations

from open_sea_v1.endpoints.assets import AssetsEndpoint, AssetsOrderBy, ClientParams
from open_sea_v1.helpers.testing_class import QueryTestCase


class TestAssetsRequest(QueryTestCase):
    endpoint = AssetsEndpoint

    @classmethod
    def setUpClass(cls) -> None:
        cls.default_client_params = ClientParams()
        cls.default_asset_params = dict(
            client_params=cls.default_client_params, token_ids=cls.token_ids, asset_contract_address=cls.sample_contract,
        )

    def test_cannot_all_be_none_owner_token_ids_asset_contract_address_asset_contract_addresses_collection(self):
        assets_kwargs = ('owner', 'token_ids', 'collection', 'asset_contract_address', 'asset_contract_addresses')
        for kwarg_combo in combinations(assets_kwargs, r=len(assets_kwargs)):
            complete_kwargs = {k: None for k in kwarg_combo} | {'client_params': self.default_client_params}
            self.assertRaises(ValueError, self.endpoint, **complete_kwargs)

    def test_param_owner_returns_assets_from_specified_owner(self):
        params = dict(owner=self.sample_wallet, order_direction='asc', **self.default_asset_params)
        for asset in self.create_and_get(**params):
            self.assertEqual(asset.owner.address, self.sample_wallet)

    def test_param_token_ids_raise_exception_if_missing_contract_address_and_addresses(self):
        self.assertRaises(ValueError, self.endpoint, token_ids=[1, 2, 3])

    def test_params_cannot_be_simultaneously_be_passed_asset_contract_address_and_contract_addresses(self):
        params = self.default_asset_params | dict(asset_contract_address=True, asset_contract_addresses=True)  # type: ignore
        self.assertRaises(ValueError, self.endpoint, **params)

    def test_param_token_ids_returns_assets_corresponding_to_single_contract(self):
        params = dict(order_direction='asc', **self.default_asset_params)
        for asset in self.create_and_get(**params):
            self.assertEqual(asset.asset_contract.address, self.sample_contract)

    def test_param_order_direction_can_only_be_asc_or_desc(self):
        invalid_order_values = (False, 0, 1, "", [], (), {}, 'hi')
        for invalid_order in invalid_order_values:
            params = dict(token_ids=[1], asset_contract_address=self.sample_contract, order_direction=invalid_order)
            self.assertRaises((ValueError, TypeError), self.endpoint, **params)

    def test_param_order_by_sale_date(self):
        params = self.default_asset_params | dict(order_by=AssetsOrderBy.SALE_DATE)
        assets_sales = [asset.last_sale.event_timestamp for asset in self.create_and_get(**params)]
        self.assertEqual(sorted(assets_sales, reverse=True), assets_sales)

    def test_param_order_by_sale_count(self):
        params = self.default_asset_params | dict(order_by=AssetsOrderBy.SALE_COUNT)
        assets_sales_cnt = [asset.num_sales for asset in self.create_and_get(**params)]
        self.assertEqual(sorted(assets_sales_cnt, reverse=True), assets_sales_cnt)

    def test_param_order_by_sale_price(self):
        params = self.default_asset_params | dict(order_by=AssetsOrderBy.SALE_PRICE)
        assets_last_sale_price = [asset.last_sale.total_price for asset in self.create_and_get(**params)]
        self.assertEqual(sorted(assets_last_sale_price, reverse=True), assets_last_sale_price)

    def test_param_order_by_visitor_count(self):
        pass  # as far as I know this is not returned in the API http_response and done directly by OpenSea

