from dataclasses import dataclass

from open_sea_v1.responses import AssetResponse
from open_sea_v1.responses.response__base import _OpenSeaAPIResponse


@dataclass
class _EventReponse(_OpenSeaAPIResponse):
    _json: dict

    def __str__(self) -> str:
        return f"{self.event_type=}, {self.total_price=}"

    def __post_init__(self):
        self.approved_account = self._json['approved_account']
        self.asset_bundle = self._json['asset_bundle']
        self.auction_type = self._json['auction_type']
        # self.big_amount = self._json['big_amount']
        self.collection_slug = self._json['collection_slug']
        self.contract_address = self._json['contract_address']
        self.created_date = self._json['created_date']
        self.custom_event_name = self._json['custom_event_name']
        self.dev_fee_payment_event = self._json['dev_fee_payment_event']
        self.duration = self._json['duration']
        self.ending_price = self._json['ending_price']
        self.event_type = self._json['event_type']
        self.from_account = self._json['from_account']
        self.id = self._json['id']
        self.owner_account = self._json['owner_account']
        self.quantity = self._json['quantity']
        self.starting_price = self._json['starting_price']
        self.to_account = self._json['to_account']
        self.total_price = self._json['total_price']
        self.bid_amount = self._json['bid_amount']

    @property
    def asset(self) -> AssetResponse:
        return AssetResponse(self._json['asset'])

    @property
    def payment_token(self) -> dict:
        return self._json['payment_token']

    @property
    def seller(self) -> dict:
        return self._json['seller']

    @property
    def transaction(self) -> dict:
        return self._json['transaction']

    @property
    def winner_account(self) -> dict:
        return self._json['winner_account']

