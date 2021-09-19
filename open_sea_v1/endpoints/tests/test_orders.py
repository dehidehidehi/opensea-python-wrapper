from unittest import TestCase
from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.orders import OrdersEndpoint
# from open_sea_v1.responses.order import OrderResponse


class TestOrdersEndpoint(TestCase):

    def setUp(self) -> None:
        self.endpoint_kwargs = dict(
            client_params=ClientParams(limit=2, max_pages=1, page_size=2),
        )

    @staticmethod
    def create_and_get(**kwargs) -> list[...]:
        orders_client = OrdersEndpoint(**kwargs)
        orders_client._get_request()
        return orders_client.parsed_http_response

    def test_attr_asset_contract_address_raises_if_not_defined_with_token_id_or_token_ids(self):
        self.endpoint_kwargs |= dict(asset_contract_address='str')
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)
        self.endpoint_kwargs |= dict(token_id=1)
        OrdersEndpoint(**self.endpoint_kwargs)
        self.endpoint_kwargs.pop('token_id')
        self.endpoint_kwargs |= dict(token_ids=[1, 2])
        OrdersEndpoint(**self.endpoint_kwargs)

    def test_attr_token_id_raises_if_not_defined_together_with_asset_contract_address(self):
        self.endpoint_kwargs |= dict(token_id=1)
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)
        self.endpoint_kwargs |= dict(asset_contract_address='str')
        OrdersEndpoint(**self.endpoint_kwargs)

    def test_attr_token_ids_raises_if_not_defined_together_with_asset_contract_address(self):
        self.endpoint_kwargs |= dict(token_ids=[1, 2])
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)
        self.endpoint_kwargs |= dict(asset_contract_address='str')
        OrdersEndpoint(**self.endpoint_kwargs)

    def test_attr_token_id_and_token_ids_cannot_be_defined_together(self):
        self.endpoint_kwargs |= dict(asset_contract_address='str', token_id=1, token_ids=[1, 2])
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)