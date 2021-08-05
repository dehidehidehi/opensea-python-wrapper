"""
Assigns attributes to dictionnary values for easier object navigation.
"""
from dataclasses import dataclass

from open_sea_v1.responses.abc import BaseResponse


@dataclass
class _CollectionStats:
    _json: dict

    def __str__(self) -> str:
        return f"({_CollectionStats.__name__}, {self.floor_price=}, {self.average_price=}, {self.market_cap=})"

    def __post_init__(self):
        self.one_day_volume = self._json["one_day_volume"]
        self.one_day_change = self._json["one_day_change"]
        self.one_day_average_price = self._json["one_day_average_price"]
        self.one_day_sales = self._json["one_day_sales"]
        self.seven_day_volume = self._json["seven_day_volume"]
        self.seven_day_change = self._json["seven_day_change"]
        self.seven_day_sales = self._json["seven_day_sales"]
        self.seven_day_average_price = self._json["seven_day_average_price"]
        self.thirty_day_volume = self._json["thirty_day_volume"]
        self.thirty_day_change = self._json["thirty_day_change"]
        self.thirty_day_sales = self._json["thirty_day_sales"]
        self.thirty_day_average_price = self._json["thirty_day_average_price"]
        self.total_volume = self._json["total_volume"]
        self.total_sales = self._json["total_sales"]
        self.total_supply = self._json["total_supply"]
        self.count = self._json["count"]
        self.num_owners = self._json["num_owners"]
        self.average_price = self._json["average_price"]
        self.num_reports = self._json["num_reports"]
        self.market_cap = self._json["market_cap"]
        self.floor_price = self._json["floor_price"]


@dataclass
class CollectionResponse(BaseResponse):
    _json: dict

    def __str__(self) -> str:
        return f"({CollectionResponse.__name__}, {self.name=}, {self.short_description=})"

    def __post_init__(self):
        self.banner_image_url = self._json["banner_image_url"]
        self.chat_url = self._json["chat_url"]
        self.created_date = self._json["created_date"]
        self.default_to_fiat = self._json["default_to_fiat"]
        self.description = self._json["description"]
        self.dev_buyer_fee_basis_points = self._json["dev_buyer_fee_basis_points"]
        self.dev_seller_fee_basis_points = self._json["dev_seller_fee_basis_points"]
        self.discord_url = self._json["discord_url"]
        self.display_data = self._json["display_data"]
        self.external_url = self._json["external_url"]
        self.featured = self._json["featured"]
        self.featured_image_url = self._json["featured_image_url"]
        self.hidden = self._json["hidden"]
        self.safelist_request_status = self._json["safelist_request_status"]
        self.image_url = self._json["image_url"]
        self.is_subject_to_whitelist = self._json["is_subject_to_whitelist"]
        self.large_image_url = self._json["large_image_url"]
        self.medium_username = self._json["medium_username"]
        self.only_proxied_transfers = self._json["only_proxied_transfers"]
        self.opensea_buyer_fee_basis_points = self._json["opensea_buyer_fee_basis_points"]
        self.opensea_seller_fee_basis_points = self._json["opensea_seller_fee_basis_points"]
        self.payout_address = self._json["payout_address"]
        self.require_email = self._json["require_email"]
        self.short_description = self._json["short_description"]
        self.slug = self._json["slug"]
        self.telegram_url = self._json["telegram_url"]
        self.twitter_username = self._json["twitter_username"]
        self.instagram_username = self._json["instagram_username"]
        self.wiki_url = self._json["wiki_url"]
        self.name = self._json["name"]

    @property
    def stats(self) -> _CollectionStats:
        return _CollectionStats(self._json['stats'])