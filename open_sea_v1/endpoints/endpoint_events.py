from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from open_sea_v1.endpoints.endpoint_abc import BaseOpenSeaEndpoint
from open_sea_v1.endpoints.endpoint_client import OpenSeaClient
from open_sea_v1.endpoints.endpoint_urls import OpenseaApiEndpoints
from open_sea_v1.helpers.extended_classes import ExtendedStrEnum
from open_sea_v1.responses import EventResponse


class EventType(ExtendedStrEnum):
    """
    The event type to filter. Can be created for new auctions, successful for sales, cancelled, bid_entered, bid_withdrawn, transfer, or approve
    """
    CREATED = 'created'
    SUCCESSFUL = 'successful'
    CANCELLED = 'cancelled'
    BID_ENTERED = 'bid_entered'
    BID_WITHDRAWN = 'bid_withdrawn'
    TRANSFER = 'transfer'
    APPROVE = 'approve'


class AuctionType(ExtendedStrEnum):
    """
    Filter by an auction type. Can be english for English Auctions, dutch for fixed-price and declining-price sell orders (Dutch Auctions), or min-price for CryptoPunks bidding auctions.
    """
    ENGLISH = 'english'
    DUTCH = 'dutch'
    MIN_PRICE = 'min-price'


@dataclass
class _EventsEndpoint(OpenSeaClient, BaseOpenSeaEndpoint):
    """
    Opensea API Events Endpoint

    Parameters
    ----------

    offset:
        Offset for pagination

    limit:
        Limit for pagination

    asset_contract_address:
        The NFT contract address for the assets for which to show events

    event_type:
        The event type to filter. Can be created for new auctions, successful for sales, cancelled, bid_entered, bid_withdrawn, transfer, or approve

    only_opensea:
        Restrict to events on OpenSea auctions. Can be true or false

    auction_type:
        Filter by an auction type. Can be english for English Auctions, dutch for fixed-price and declining-price sell orders (Dutch Auctions), or min-price for CryptoPunks bidding auctions.

    occurred_before:
        Only show events listed before this datetime.

    occurred_after:
        Only show events listed after this datetime.

    api_key:
        Optional Opensea API key, if you have one.

    :return: Parsed JSON
    """
    offset: int
    limit: int
    asset_contract_address: str
    event_type: EventType
    only_opensea: bool
    collection_slug: Optional[str] = None
    token_id: Optional[str] = None
    account_address: Optional[str] = None
    auction_type: Optional[AuctionType] = None
    occurred_before: Optional[datetime] = None
    occurred_after: Optional[datetime] = None
    api_key: Optional[str] = None

    def __post_init__(self):
        self._validate_request_params()

    @property
    def url(self) -> str:
        return OpenseaApiEndpoints.EVENTS.value

    @property
    def _request_params(self) -> dict:
        params = dict(offset=self.offset, limit=self.limit, asset_contract_address=self.asset_contract_address, event_type=self.event_type, only_opensea=self.only_opensea, collection_slug=self.collection_slug, token_id=self.token_id, account_address=self.account_address, auction_type=self.auction_type, occurred_before=self.occurred_before, occurred_after=self.occurred_after)
        return dict(api_key=self.api_key, params=params)

    def get_request(self, **kwargs):
        self._response = self._get_request(self.url, **self._request_params)

    @property
    def response(self) -> list[EventResponse]:
        self._assert_get_request_was_called_before_accessing_this_property()
        events_json = self._response.json()['asset_events']
        events = [EventResponse(event) for event in events_json]
        return events

    def _validate_request_params(self) -> None:
        self._validate_param_auction_type()
        self._validate_param_event_type()
        self._validate_params_occurred_before_and_occurred_after()

    def _validate_param_event_type(self) -> None:
        if not isinstance(self.event_type, (str, EventType)):
            raise TypeError('Invalid event_type type. Must be str or EventType Enum.', f"{self.event_type=}")

        if self.event_type not in EventType.list():
            raise ValueError('Invalid event_type value. Must be str value from EventType Enum.', f"{self.event_type=}")

    def _validate_param_auction_type(self) -> None:
        if self.auction_type is None:
            return

        if not isinstance(self.auction_type, (str, AuctionType)):
            raise TypeError('Invalid auction_type type. Must be str or AuctionType Enum.', f"{self.auction_type=}")

        if self.auction_type not in AuctionType.list():
            raise ValueError('Invalid auction_type value. Must be str value from AuctionType Enum.',
                             f"{self.auction_type=}")

    def _validate_params_occurred_before_and_occurred_after(self) -> None:
        self._validate_param_occurred_before()
        self._validate_param_occurred_after()
        if self.occurred_after and self.occurred_before:
            self._assert_param_occurred_before_after_cannot_be_same_value()
            self._assert_param_occurred_before_cannot_be_higher_than_occurred_after()

    def _validate_param_occurred_before(self) -> None:
        if not isinstance(self.occurred_before, (type(None), datetime)):
            raise TypeError('Invalid occurred_before type. Must be instance of datetime.',
                            f'{type(self.occurred_before)=}')

    def _validate_param_occurred_after(self) -> None:
        if not isinstance(self.occurred_after, (type(None), datetime)):
            raise TypeError('Invalid occurred_after type. Must be instance of datetime.',
                            f'{type(self.occurred_after)=}')

    def _assert_param_occurred_before_after_cannot_be_same_value(self) -> None:
        if self.occurred_after == self.occurred_before:
            raise ValueError('Params occurred_after and occurred_before may not have the same value.',
                             f"{self.occurred_before=}, {self.occurred_after=}")

    def _assert_param_occurred_before_cannot_be_higher_than_occurred_after(self) -> None:
        if not self.occurred_after < self.occurred_before:
            raise ValueError('Param occurred_before cannot be higher than param occurred_after.',
                             f"{self.occurred_before=}, {self.occurred_after=}")