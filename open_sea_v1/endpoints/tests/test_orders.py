import logging
from datetime import datetime
from unittest import TestCase

from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.orders import OrdersEndpoint
from open_sea_v1.responses.order import OrderResponse

logger = logging.getLogger(__name__)


class TestOrdersEndpoint(TestCase):

    def setUp(self) -> None:
        self.asset_contract_address = '0x3f4a885ed8d9cdf10f3349357e3b243f3695b24a'
        self.owner_address = '0x85844112d2f9cfe2254188b4ee69edd942fad32d'
        self.token_id = 3263
        self.token_id_2 = 8797
        self.endpoint_kwargs = dict(
            client_params=ClientParams(limit=5, max_pages=1),
            # listed_after=datetime(year=2021, month=8, day=15),
            # listed_before=datetime(year=2021, month=8, day=20),
        )

    @staticmethod
    def create_and_get(**kwargs) -> list[OrderResponse]:
        orders_client = OrdersEndpoint(**kwargs)
        orders_client._get_request()
        return orders_client.parsed_http_response

    def test_attr_asset_contract_address_raises_if_not_defined_with_token_id(self):
        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address)
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)
        self.endpoint_kwargs |= dict(token_id=self.token_id)
        OrdersEndpoint(**self.endpoint_kwargs)

    def test_attr_asset_contract_address_raises_if_not_defined_with_token_ids(self):
        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address, token_ids=[self.token_id, self.token_id_2])
        OrdersEndpoint(**self.endpoint_kwargs)

    def test_attr_token_id_raises_if_not_defined_together_with_asset_contract_address(self):
        self.endpoint_kwargs |= dict(token_id=self.token_id)
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)

    def test_attr_token_ids_raises_if_len_is_above_30(self):
        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address, token_ids=list(range(1, 32)))
        self.assertRaises(ValueError, OrdersEndpoint, **self.endpoint_kwargs)

    def test_attr_token_ids_raises_if_not_defined_together_with_asset_contract_address(self):
        self.endpoint_kwargs |= dict(token_ids=[self.token_id, self.token_id_2])
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)
        self.endpoint_kwargs |= dict(asset_contract_address='str')
        OrdersEndpoint(**self.endpoint_kwargs)

    def test_attr_token_id_and_token_ids_cannot_be_defined_together(self):
        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address, token_id=1, token_ids=[self.token_id, self.token_id_2])
        self.assertRaises(AttributeError, OrdersEndpoint, **self.endpoint_kwargs)

    def test_response_returns_order_object(self):
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        self.assertIsInstance(resp, list)
        self.assertIsInstance(resp[0], OrderResponse)

    def test_attr_asset_contract_address_returns_correct_contract_address_orders(self):
        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address, token_id=self.token_id)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        self.assertEqual(resp[0].asset.asset_contract.address, self.endpoint_kwargs['asset_contract_address'])

    def test_attr_payment_token_address_returns_correct_payment_token_address_orders(self):
        weth_payment_token_address = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
        # https://etherscan.io/token/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2
        self.endpoint_kwargs |= dict(payment_token_address=weth_payment_token_address)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        self.assertEqual(weth_payment_token_address, resp[0].payment_token_contract['address'])

    def test_attr_maker_address_correctly_returns_only_orders_made_by_maker_address(self):
        """
        A maker is the first mover in a trade.
        Makers either declare intent to sell an item,
        or they declare intent to buy by bidding on one.
        https://docs.opensea.io/reference/terminology
        """
        random_buyer_address = '0xdcfd6d6e63f15a391d96d1b76575ae39ad6965d9'
        self.endpoint_kwargs |= dict(maker=random_buyer_address)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        self.assertEqual(random_buyer_address, resp[0].maker['address'])

    def test_attr_taker_address_correctly_returns_only_orders_made_by_taker_address(self):
        """
        A taker is the counterparty who responds to a
        maker's order by, respectively, either buying the
         item or accepting a bid on it.
        https://docs.opensea.io/reference/terminology

        Observations from the maintainer:
        # It would seem on OpenSea that all takers are actually OpenSea, as the platform acts
        # as a middle-man. I am unsure of this and would greatly appreciate community feedback!
        # https://github.com/dehidehidehi/opensea-python-wrapper/issues
        """
        logger.warning("\nThe 'taker' parameter may cause confusion, please read test docstring and comments.")
        open_sea_default_address = '0x0000000000000000000000000000000000000000'
        self.endpoint_kwargs |= dict(taker=open_sea_default_address)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        self.assertEqual(open_sea_default_address, resp[0].taker['address'])

    def test_attr_is_english_returns_only_orders_from_english_auctions(self):
        """
        Maintainer observations:
        This is not fully testable, as per the documentation.
        We can only assert that all responses have a zero value for the sale_kind attribute.

        Observation 2:
        Setting the is_english attr to False does NOT return only dutch auctions.
        In this case, use : sale_kind = 1

        Documentation:
        'Filter by the kind of sell order. 0 for fixed-price sales or min-bid auctions, and 1 for declining-price Dutch Auctions. NOTE: use only_english=true for filtering for only English Auctions'
        """
        self.endpoint_kwargs |= dict(is_english=True)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(all(r.sale_kind == 0 for r in resp))

    def test_attr_bundled_returns_only_bundled_orders(self):
        self.endpoint_kwargs |= dict(bundled=True)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        self.assertTrue(all(r.asset_bundle for r in resp))

    def test_attr_include_bundled_raises_if_not_set_together_with_token_id_or_token_ids(self):
        self.endpoint_kwargs |= dict(include_bundled=True)
        self.assertRaises(AttributeError, self.create_and_get, **self.endpoint_kwargs)

    def test_attr_include_bundled_cannot_be_true_without_asset_contract_address_or_owner_address(self):
        self.endpoint_kwargs |= dict(include_bundled=True, token_id=self.token_id)
        self.assertRaises(AttributeError, self.create_and_get, **self.endpoint_kwargs)

    def test_attr_include_bundled_does_not_raise_when_false_without_asset_contract_address_or_owner_address(self):
        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address, include_bundled=False, token_id=self.token_id)
        self.create_and_get(**self.endpoint_kwargs)

    def test_attr_include_bundled_returns_all_assets_which_share_the_same_asset_contract_address(self):
        client_params = ClientParams(page_size=10, limit=1, max_pages=1)
        self.endpoint_kwargs |= dict(client_params=client_params, include_bundled=True, asset_contract_address=self.asset_contract_address, token_id=self.token_id)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(resp)
        all_have_same_contract_address: bool = len(set(r.asset.asset_contract.address for r in resp)) == 1
        self.assertTrue(all_have_same_contract_address)

    def test_attr_include_bundled_returns_all_assets_which_share_the_same_owner_address(self):
        """
        This is difficult to test. You need to find a very specific set of assets and bundles.
        Would appreciate some help from the community to find something here that does NOT return an empty response.
        https://github.com/dehidehidehi/opensea-python-wrapper/issues
        """
        logger.warning("\nThe 'include_bundled' set together with 'owner' address is untested, please read test docstring and comments.")
        # client_params = ClientParams(page_size=10, limit=1, max_pages=1)
        # self.endpoint_kwargs |= dict(client_params=client_params,  owner=self.owner_address, asset_contract_address=self.asset_contract_address, token_id=9180, include_bundled=True)
        # resp = self.create_and_get(**self.endpoint_kwargs)
        # self.assertTrue(resp)
        # all_have_same_owner_address: bool = len(set(r.asset.owner.address for r in resp)) == 1
        # self.assertTrue(all_have_same_owner_address)

    def test_attr_include_invalid_returns_also_invalid_orders(self):
        """
        Include orders marked invalid by the orderbook, typically due to makers not owning enough of the token/asset anymore.
        """
        logger.warning("\nAttribute 'include_invalid' is untested.")

    def test_attr_listed_after_raises_if_is_not_instance_of_datetime(self):
        string_datetime = datetime.now().isoformat()
        self.endpoint_kwargs |= dict(listed_after=string_datetime)
        self.assertRaises(TypeError, self.create_and_get, **self.endpoint_kwargs)

    def test_attr_listed_after_returns_only_orders_after_specified_datetime(self):
        date_ref = datetime(year=2021, month=8, day=15)
        self.endpoint_kwargs |= dict(listed_after=date_ref)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(all(r.created_date > date_ref for r in resp))

    def test_attr_listed_before_returns_only_orders_before_specified_datetime(self):
        date_ref = datetime(year=2021, month=8, day=14)
        self.endpoint_kwargs |= dict(listed_before=date_ref)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(all(r.created_date <= date_ref for r in resp))

    def test_attr_listed_after_and_listed_before_work_together(self):
        older_thresh = datetime(year=2021, month=8, day=10)
        recent_thresh = datetime(year=2021, month=8, day=15)
        self.endpoint_kwargs |= dict(listed_before=recent_thresh, listed_after=older_thresh)
        resp = self.create_and_get(**self.endpoint_kwargs)
        self.assertTrue(all(older_thresh <= r.created_date <= recent_thresh for r in resp))

    def test_attr_side_not_raises_if_valid_value(self):
        for valid_value in {None, 1, 0}:
            self.endpoint_kwargs |= dict(side=valid_value)
            self.create_and_get(**self.endpoint_kwargs)

    def test_attr_side_raises_if_invalid_value(self):
        for invalid_value in {'string', -1, 0.0, 1.0, 2}:
            self.endpoint_kwargs |= dict(side=invalid_value)
            self.assertRaises(ValueError, self.create_and_get, **self.endpoint_kwargs)

    def test_sale_kind_not_raises_if_valid_value(self):
        for valid_value in {None, 1, 0}:
            self.endpoint_kwargs |= dict(sale_kind=valid_value)
            self.create_and_get(**self.endpoint_kwargs)

    def test_attr_sale_kind_raises_if_invalid_value(self):
        for invalid_value in {'string', -1, 0.0, 1.0, 2}:
            self.endpoint_kwargs |= dict(sale_kind=invalid_value)
            self.assertRaises(ValueError, self.create_and_get, **self.endpoint_kwargs)

    def test_attr_order_by_not_raises_if_valid_value(self):
        self.endpoint_kwargs |= dict(order_by='created_date')
        self.create_and_get(**self.endpoint_kwargs)

        self.endpoint_kwargs |= dict(asset_contract_address=self.asset_contract_address, token_id=self.token_id, order_by='eth_price')
        self.create_and_get(**self.endpoint_kwargs)

    def test_attr_order_by_raises_if_invalid_value(self):
        for invalid_value in {'asc', -1, 'desc'}:
            self.endpoint_kwargs |= dict(order_by=invalid_value)
            self.assertRaises(ValueError, self.create_and_get, **self.endpoint_kwargs)

    def test_attr_order_by_eth_price_raises_if_asset_contract_address_and_token_id_are_not_defined(self):
        self.endpoint_kwargs |= dict(order_by='eth_price')
        self.assertRaises(AttributeError, self.create_and_get, **self.endpoint_kwargs)

    def test_attr_order_direction_not_raises_if_valid_value(self):
        for valid_value in {None, 'asc', 'desc'}:
            self.endpoint_kwargs |= dict(order_direction=valid_value)
            self.create_and_get(**self.endpoint_kwargs)

    def test_attr_order_direction_raises_if_invalid_value(self):
        for invalid_value in {'up', -1, False}:
            self.endpoint_kwargs |= dict(order_direction=invalid_value)
            self.assertRaises(ValueError, self.create_and_get, **self.endpoint_kwargs)
