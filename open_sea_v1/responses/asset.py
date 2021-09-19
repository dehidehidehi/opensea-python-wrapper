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
        self.sell_orders = self._json.get("sell_orders")

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
    def creator(self) -> Optional[dict]:
        return self._json.get('creator')
