"""
Assigns attributes to dictionnary values for easier object navigation.
"""
from dataclasses import dataclass

from open_sea_v1.responses.response_abc import _OpenSeaResponse
from open_sea_v1.responses.response_collection import _CollectionResponse


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
class _AssetResponse(_OpenSeaResponse):
    _json: dict

    def __str__(self) -> str:
        return f"({_AssetResponse.__name__}, id={self.token_id.zfill(5)}, name={self.name})"

    def __post_init__(self):
        self._set_common_attrs()
        self._set_optional_attrs()

    def _set_common_attrs(self):
        self.token_id = self._json["token_id"]
        self.num_sales = self._json["num_sales"]
        self.background_color = self._json["background_color"]
        self.image_url = self._json["image_url"]
        self.image_preview_url = self._json["image_preview_url"]
        self.image_thumbnail_url = self._json["image_thumbnail_url"]
        self.image_original_url = self._json["image_original_url"]
        self.animation_url = self._json["animation_url"]
        self.animation_original_url = self._json["animation_original_url"]
        self.name = self._json["name"]
        self.description = self._json["description"]
        self.external_link = self._json["external_link"]
        self.permalink = self._json["permalink"]
        self.decimals = self._json["decimals"]
        self.token_metadata = self._json["token_metadata"]
        self.id = self._json["id"]

    def _set_optional_attrs(self):
        """
        Most asset responses are alike, but some are returned with less information.
        To avoid raising KeyErrors, we will use the .get method when setting these attributes.
        """
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
    def traits(self) -> list[_Traits]:
        return [_Traits(traits) for traits in self._json['traits']]

    @property
    def last_sale(self) -> _LastSale:
        return _LastSale(self._json['last_sale'])

    @property
    def collection(self):
        return _CollectionResponse(self._json['collection'])

    @property
    def creator(self) -> dict:
        return self._json['creator']
