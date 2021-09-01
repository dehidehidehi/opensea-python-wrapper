from dataclasses import dataclass
from datetime import datetime

from open_sea_v1.endpoints.abc import BaseEndpoint
from open_sea_v1.endpoints.client import BaseClient, ClientParams
from open_sea_v1.endpoints.urls import EndpointURLS
from open_sea_v1.responses.collection import CollectionResponse
from open_sea_v1.responses.order import OrderResponse


@dataclass
class OrdersEndpoint(BaseClient, BaseEndpoint):
    """
    How to fetch orders from the OpenSea system.

    Parameters
    ----------
    client_params:
        ClientParams instance.

    asset_contract_address: str
        Filter by smart contract address for the asset category.
        Needs to be defined together with token_id or token_ids.

    payment_token_address: str
        Filter by the address of the smart contract of the payment
        token that is accepted or offered by the order

    maker: str
        Filter by the order maker's wallet address

    taker: str
        Filter by the order taker's wallet address.
        Orders open for any taker have the null address as their taker.

    owner: str
        Filter by the asset owner's wallet address

    is_english: bool
        When "true", only show English Auction sell orders, which wait for the highest bidder.
        When "false", exclude those.

    bundled: bool
        Only show orders for bundles of assets

    include_bundled: bool
        Include orders on bundles where all assets in the bundle share the address
        provided in asset_contract_address or where the bundle's maker is the address provided in owner.

    include_invalid: bool
        Include orders marked invalid by the orderbook, typically due to makers
        not owning enough of the token/asset anymore.

    listed_after: datetime
        Only show orders listed after this timestamp.

    listed_before: datetime
        Only show orders listed before this timestamp.

    token_id: str
        Filter by the token ID of the order's asset.
        Needs to be defined together with asset_contract_address.

    token_ids: list[str]
        Filter by a list of token IDs for the order's asset.
        Needs to be defined together with asset_contract_address.

    side: int
        Filter by the side of the order.
        0 for buy orders and 1 for sell orders.

    sale_kind: int
        Filter by the kind of sell order.
        0 for fixed-price sales or min-bid auctions, and 1 for declining-price Dutch Auctions.
        NOTE=use only_english=true for filtering for only English Auctions

    limit: int
        Number of orders to return (capped at 50).

    offset: int
        Number of orders to offset by (for pagination)

    order_by: str
        How to sort the orders. Can be created_date for when they were made,
        or eth_price to see the lowest-priced orders first (converted to their ETH values).
        eth_price is only supported when asset_contract_address and token_id are also defined.

    order_direction: str
        Can be asc or desc for ascending or descending sort.
        For example, to see the cheapest orders, do order_direction asc and order_by eth_price.

    :return=Parsed JSON
    """
    client_params: ClientParams = None
    asset_contract_address: str = None
    payment_token_address: str = None
    maker: str = None
    taker: str = None
    owner: str = None
    is_english: bool = None
    bundled: bool = None
    include_bundled: bool = None
    include_invalid: bool = None
    listed_after: datetime = None
    listed_before: datetime = None
    token_id: str = None
    token_ids: list[str] = None
    side: int = None
    sale_kind: int = None
    order_by: str = 'created_date'
    order_direction: str = 'desc'

    def __post_init__(self):
        self._validate_request_params()

    @property
    def url(self):
        return EndpointURLS.ORDERS.value

    @property
    def parsed_http_response(self) -> list[OrderResponse]:
        return self.parse_http_response(OrderResponse, 'orders')

    def _get_request(self, **kwargs):
        params = dict(
            asset_contract_address=self.asset_contract_address,
            payment_token_address=self.payment_token_address,
            maker=self.maker,
            taker=self.taker,
            owner=self.owner,
            is_english=self.is_english,
            bundled=self.bundled,
            include_bundled=self.include_bundled,
            include_invalid=self.include_invalid,
            listed_after=self.listed_after,
            listed_before=self.listed_before,
            token_id=self.token_id,
            token_ids=self.token_ids,
            side=self.side,
            sale_kind=self.sale_kind,
            limit=self.client_params.limit,
            offset=self.client_params.offset,
            order_by=self.order_by,
            order_direction=self.order_direction,
        )
        get_request_kwargs = dict(params=params)
        self._http_response = super()._get_request(**get_request_kwargs)
        return self._http_response

    def _validate_request_params(self) -> None:
        self._validate_values(self.side, attr_name='side', valid_values=[None, 1, 0])
        self._validate_values(self.sale_kind, attr_name='sale_kind', valid_values=[None, 1, 0])
        self._validate_values(self.order_by, attr_name='order_by', valid_values=[None, 'created_date', 'eth_price'])
        self._validate_values(self.order_direction, attr_name='order_direction', valid_values=[None, 'asc', 'desc'])

        self._validate_contract_address_defined_with_token_id_or_tokens_ids()
        self._validate_token_id_defined_with_contract_address()
        self._validate_token_ids_defined_with_contract_address()
        self._validate_token_ids_quantity_is_lower_or_equal_to_30()
        self._validate_token_id_and_token_ids_cannot_be_defined_together()
        self._validate_listed_after_and_listed_before_are_datetimes()
        self._validate_order_by_eth_price_is_defined_with_asset_contract_address_and_token_id_or_token_ids()

        if self.include_bundled:
            self._validate_include_bundled_is_defined_with_contract_address_or_owner_address()
            self._validate_include_bundled_is_defined_with_token_id_or_token_ids()

    def _validate_contract_address_defined_with_token_id_or_tokens_ids(self) -> None:
        if self.asset_contract_address is None:
            return
        if not any([self.token_id, self.token_ids]):
            raise AttributeError('Attribute asset_contract_address must be defined together with either token_id or token_ids.')

    def _validate_token_id_defined_with_contract_address(self) -> None:
        if self.token_id is None:
            return
        if not self.asset_contract_address:
            raise AttributeError('Attribute token_id must be defined together with asset_contract_address')

    def _validate_token_ids_quantity_is_lower_or_equal_to_30(self):
        if self.token_ids and len(self.token_ids) > 30:
            raise ValueError('Attribute token_ids length must be equal or below 30.')

    def _validate_token_ids_defined_with_contract_address(self) -> None:
        if self.token_ids is None:
            return
        if not self.asset_contract_address:
            raise AttributeError('Attribute token_ids must be defined together with asset_contract_address')

    def _validate_token_id_and_token_ids_cannot_be_defined_together(self) -> None:
        if self.token_ids and self.token_id:
            raise AttributeError('Attribute token_id and token_ids cannot be defined together.')

    def _validate_include_bundled_is_defined_with_contract_address_or_owner_address(self) -> None:
        if not any([self.asset_contract_address, self.owner]):
            raise AttributeError('Attribute include_bundled must be defined together with asset_contract_address or owner')

    def _validate_include_bundled_is_defined_with_token_id_or_token_ids(self):
        if not any([self.token_id, self.token_ids]):
            raise AttributeError(
                'Attribute include_bundled must be defined together with token_id or token_ios')

    def _validate_listed_after_and_listed_before_are_datetimes(self):
        if not isinstance(self.listed_after, (type(None), datetime)):
            raise TypeError("Attribute 'listed_after' must be a datetime instance")

        if not isinstance(self.listed_before, (type(None), datetime)):
            raise TypeError("Attribute 'listed_before' must be a datetime instance")

    def _validate_order_by_eth_price_is_defined_with_asset_contract_address_and_token_id_or_token_ids(self):
        if not self.order_by:
            return

        if not self.asset_contract_address and self.order_by == 'eth_price' and not any([self.token_id, self.token_ids]):
            raise AttributeError("When attribute 'order_by' is set to 'eth_price', you must also set the asset_contract_address and token_id or token_ids attributes.")

    @staticmethod
    def _validate_values(attr, *, attr_name: str, valid_values: list):
        if not any(attr is v for v in valid_values):
            raise ValueError(f"attr {attr_name} must be a value among: {valid_values}")
