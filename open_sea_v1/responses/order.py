"""
Assigns attributes to dictionnary values for easier object navigation.
"""
from dataclasses import dataclass

from open_sea_v1.responses.abc import BaseResponse
from open_sea_v1.responses.asset import AssetResponse


@dataclass
class OrderResponse(BaseResponse):
    _json: dict

    def __str__(self):
        return f"order_id={self.id}"

    def __post_init__(self):
        self._set_common_attrs()
        self._set_optional_attrs()

    def _set_common_attrs(self):
        self.id = self._json['id']
        self.asset_bundle = self._json['asset_bundle']
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

    @property
    def asset(self) -> AssetResponse:
        return AssetResponse(self._json['asset'])

    def _set_optional_attrs(self):
        """
        Most asset responses are alike, but some are returned with less information.
        To avoid raising KeyErrors, we will use the .get method when setting these attributes.
        """
        ...
