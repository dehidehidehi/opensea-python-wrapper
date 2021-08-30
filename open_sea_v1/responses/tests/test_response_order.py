from open_sea_v1.endpoints.abc import ClientParams
from open_sea_v1.endpoints.orders import OrdersEndpoint
from open_sea_v1.responses.tests._response_helpers import ResponseTestHelper


class TestOrderObj(ResponseTestHelper):

    default_asset_params = dict(
        asset_contract_address='0x3f4a885ed8d9cdf10f3349357e3b243f3695b24a',  # incognito nft
        token_id=7504,
        side=0,
    )

    @classmethod
    def setUpClass(cls) -> None:
        client_params = ClientParams(page_size=2, limit=2)
        params = cls.default_asset_params | dict(client_params=client_params)
        cls.orders = cls.create_and_get(OrdersEndpoint, **params)
        cls.order = cls.orders[0]

    def test_attributes_do_not_raise_unexpected_exceptions(self):
        self.assert_attributes_do_not_raise_unexpected_exceptions(self.order)

    def test_no_missing_class_attributes_from_original_json_keys(self):
        self.assert_no_missing_class_attributes_from_original_json_keys(response_obj=self.order, json=self.order._json)
