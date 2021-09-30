"""
Assigns attributes to dictionnary values for easier object navigation.
"""
from dataclasses import dataclass
from typing import Optional

from open_sea_v1.responses.abc import BaseResponse
from open_sea_v1.responses.collection import CollectionResponse


@dataclass
class _LastSale:
    _last_sale: dict

    def __str__(self) -> str:
        return f"({_LastSale.__name__}, asset={self.asset}, date={self.event_timestamp}, quantity={self.quantity})"

    def __post_init__(self):
        self.asset: dict = self._last_sale['asset']
        self.asset_bundle = self._last_sale['asset_bundle']
        self.event_type = self._last_sale['event_type']
        self.event_timestamp = self._last_sale['event_timestamp']
        self.auction_type = self._last_sale['auction_type']
        self.total_price = self._last_sale['total_price']
        self.created_date = self._last_sale['created_date']
        self.quantity = self._last_sale['quantity']

    @property
    def transaction(self) -> dict:
        return self._last_sale['transaction']

    @property
    def payment_token(self) -> dict:
        return self._last_sale['payment_token']


@dataclass
class _Traits:
    _traits: dict

    def __post_init__(self):
        self.trait_type = self._traits['trait_type']
        self.value = self._traits['value']
        self.display_type = self._traits['display_type']


@dataclass
class _Owner:
    _owner: dict

    def __str__(self) -> str:
        return f"({_Owner.__name__}, user={self.user['username']})"

    def __post_init__(self):
        self.address = self._owner['address']
        self.config = self._owner['config']
        self.profile_img_url = self._owner['profile_img_url']
        self.user: dict = self._owner['user']


@dataclass
class _Contract:
    _contract: dict

    def __str__(self) -> str:
        return f"({_Contract.__name__} - {self.name.title()}: {self.description})"

    def __post_init__(self):
        self.address = self._contract['address']
        self.name = self._contract['name']
        self.symbol = self._contract['symbol']
        self.image_url = self._contract['image_url']
        self.description = self._contract['description']
        self.external_link = self._contract['external_link']


@dataclass
class OrderResponse(BaseResponse):
    _json: dict

    def __str__(self):
        return f"{self.id=}" if self.id else f"{self.order_hash=}"

    def __post_init__(self):
        self._set_optional_attrs()
        self._set_common_attrs()

    @property
    def asset(self) -> 'AssetResponse':
        return AssetResponse(self._json['asset'])

    def _set_optional_attrs(self):
        """Depending on the endpoint you use, the Order response object will contain optional attributes."""
        self.id: Optional = self._json.get('id')  # id is only provided if you use the OrdersEndpoint
        self.asset_bundle = self._json.get('asset_bundle')

    def _set_common_attrs(self):
        self.order_hash = self._json.get('order_hash')
        self.created_date = self._json['created_date']
        self.closing_date = self._json['closing_date']
        self.closing_extendable = self._json['closing_extendable']
        self.expiration_time = self._json['expiration_time']
        self.listing_time = self._json['listing_time']
        self.order_hash = self._json['order_hash']
        self.exchange = self._json['exchange']
        self.current_price = self._json['current_price']
        self.current_bounty = self._json['current_bounty']
        self.bounty_multiple = self._json['bounty_multiple']
        self.maker_relayer_fee = self._json['maker_relayer_fee']
        self.taker_relayer_fee = self._json['taker_relayer_fee']
        self.maker_protocol_fee = self._json['maker_protocol_fee']
        self.taker_protocol_fee = self._json['taker_protocol_fee']
        self.maker_referrer_fee = self._json['maker_referrer_fee']
        self.fee_method = self._json['fee_method']
        self.side = self._json['side']
        self.sale_kind = self._json['sale_kind']
        self.target = self._json['target']
        self.how_to_call = self._json['how_to_call']
        self.calldata = self._json['calldata']
        self.replacement_pattern = self._json['replacement_pattern']
        self.static_target = self._json['static_target']
        self.static_extradata = self._json['static_extradata']
        self.payment_token = self._json['payment_token']
        self.base_price = self._json['base_price']
        self.extra = self._json['extra']
        self.quantity = self._json['quantity']
        self.salt = self._json['salt']
        self.v = self._json['v']
        self.r = self._json['r']
        self.s = self._json['s']
        self.approved_on_chain = self._json['approved_on_chain']
        self.cancelled = self._json['cancelled']
        self.finalized = self._json['finalized']
        self.marked_invalid = self._json['marked_invalid']
        self.prefixed_hash = self._json['prefixed_hash']
        self.metadata: dict = self._json['metadata']
        self.maker: dict = self._json['maker']
        self.taker: dict = self._json['taker']
        self.fee_recipient: dict = self._json['fee_recipient']
        self.payment_token_contract: dict = self._json['payment_token_contract']


@dataclass
class AssetResponse(BaseResponse):
    _json: dict

    def __str__(self):
        id_str = f"token_id={self.token_id.zfill(5)}"
        name = f"name={self.name}"
        return "    ".join([id_str, name])

    def __post_init__(self):
        self._set_common_attrs()

    def _set_common_attrs(self):
        """
        Depending on the EventType you request, some elements of the json response will be missing.
        For that reason we use .get() on every element.
        """
        self.token_id = str(self._json.get("token_id") or '')
        self.num_sales = self._json.get("num_sales")
        self.background_color = self._json.get("background_color")
        self.image_url = self._json.get("image_url")
        self.image_preview_url = self._json.get("image_preview_url")
        self.image_thumbnail_url = self._json.get("image_thumbnail_url")
        self.image_original_url = self._json.get("image_original_url")
        self.animation_url = self._json.get("animation_url")
        self.animation_original_url = self._json.get("animation_original_url")
        self.name = self._json.get("name")
        self.description = self._json.get("description")
        self.external_link = self._json.get("external_link")
        self.permalink = self._json.get("permalink")
        self.decimals = self._json.get("decimals")
        self.token_metadata = self._json.get("token_metadata")
        self.id = str(self._json.get("id") or '')
        self.transfer_fee = self._json.get("transfer_fee")
        self.transfer_fee_payment_token = self._json.get("transfer_fee_payment_token")
        self.is_presale = self._json.get("is_presale")
        self.listing_date = self._json.get("listing_date")
        self.top_bid = self._json.get("top_bid")

    @property
    def asset_contract(self) -> _Contract:
        return _Contract(self._json['asset_contract'])

    @property
    def owner(self) -> _Owner:
        return _Owner(self._json['owner'])

    @property
    def traits(self) -> Optional[list[_Traits]]:
        traits = self._json.get('traits')
        if traits:
            return [_Traits(traits) for traits in self._json['traits']]
        return None

    @property
    def last_sale(self) -> Optional[_LastSale]:
        last_sale = self._json.get('last_sale')
        if last_sale:
            return _LastSale(self._json['last_sale'])
        return None

    @property
    def collection(self):
        return CollectionResponse(self._json['collection'])

    @property
    def sell_orders(self) -> Optional[list[OrderResponse]]:
        if sell_orders := self._json.get('sell_orders'):
            return [OrderResponse(order) for order in sell_orders]
        return None

    @property
    def creator(self) -> Optional[dict]:
        return self._json.get('creator')
