from dataclasses import dataclass
from enum import Enum
from typing import Optional

from requests import Response

from open_sea_v1.endpoints.endpoint_urls import OpenseaApiEndpoints
from open_sea_v1.endpoints.endpoint_client import OpenSeaClient
from open_sea_v1.endpoints.endpoint_abc import BaseOpenSeaEndpoint
from open_sea_v1.responses.asset_obj import _AssetResponse


class _AssetsOrderBy(str, Enum):
    """
    Helper Enum for remembering the possible values for the order_by param of the AssetsEndpoint class.
    """
    TOKEN_ID = "token_id"
    SALE_DATE = "sale_date"
    SALE_COUNT = "sale_count"
    VISITOR_COUNT = "visitor_count"
    SALE_PRICE = "sale_price"


@dataclass
class _AssetsEndpoint(OpenSeaClient, BaseOpenSeaEndpoint):
    """
    Opensea API Assets Endpoint

    Parameters
    ----------
    width:
        width of the snake

    owner:
        The address of the owner of the assets

    token_ids:
        List of token IDs to search for

    asset_contract_address:
        The NFT contract address for the assets

    asset_contract_addresses:
        List of contract addresses to search for. Will return a list of assets with contracts matching any of the addresses in this array. If "token_ids" is also specified, then it will only return assets that match each (address, token_id) pairing, respecting order.

    order_by:
        How to order the assets returned. By default, the API returns the fastest ordering (contract address and token id). Options you can set are token_id, sale_date (the last sale's transaction's timestamp), sale_count (number of sales), visitor_count (number of unique visitors), and sale_price (the last sale's total_price)

    order_direction:
        Can be asc for ascending or desc for descending

    offset:
        Offset

    limit:
        Defaults to 20, capped at 50.

    collection:
        Limit responses to members of a collection. Case sensitive and must match the collection slug exactly. Will return all assets from all contracts in a collection.

    :return: Parsed JSON
    """
    api_key: Optional[str] = None
    owner: Optional[str] = None
    token_ids: Optional[list[int]] = None
    asset_contract_address: Optional[list[str]] = None
    asset_contract_addresses: Optional[str] = None
    collection: Optional[str] = None
    order_by: Optional[_AssetsOrderBy] = None
    order_direction: str = None
    offset: int = 0
    limit: int = 20

    def __post_init__(self):
        self.validate_request_params()
        self._response: Optional[Response] = None

    @property
    def http_response(self):
        self._validate_response_property()
        return self._response

    @property
    def response(self) -> list[_AssetResponse]:
        self._validate_response_property()
        assets_json = self._response.json()['assets']
        assets = [_AssetResponse(asset_json) for asset_json in assets_json]
        return assets

    @property
    def url(self):
        return OpenseaApiEndpoints.ASSETS.value

    def get_request(self, *args, **kwargs):
        self._response = super().get_request(self.url, **self._request_params)

    @property
    def _request_params(self) -> dict[dict]:
        params = dict(
            owner=self.owner, token_ids=self.token_ids, asset_contract_address=self.asset_contract_address,
            asset_contract_addresses=self.asset_contract_addresses, collection=self.collection,
            order_by=self.order_by, order_direction=self.order_direction, offset=self.offset, limit=self.limit
        )
        return dict(api_key=self.api_key, params=params)

    def validate_request_params(self) -> None:
        self._validate_mandatory_params()
        self._validate_asset_contract_addresses()
        self._validate_order_direction()
        self._validate_order_by()
        self._validate_limit()

    def _validate_response_property(self):
        if self._response is None:
            raise AttributeError('You must call self.request prior to accessing self.response')

    def _validate_mandatory_params(self):
        mandatory = self.owner, self.token_ids, self.asset_contract_address, self.asset_contract_addresses, self.collection
        if all((a is None for a in mandatory)):
            raise ValueError("At least one of the following parameters must not be None:\n"
                             "owner, token_ids, asset_contract_address, asset_contract_addresses, collection")

    def _validate_asset_contract_addresses(self):
        if self.asset_contract_address and self.asset_contract_addresses:
            raise ValueError(
                "You cannot simultaneously get_request for a single contract_address and a list of contract_addresses."
            )

        if self.token_ids and not (self.asset_contract_address or self.asset_contract_addresses):
            raise ValueError(
                "You cannot query for token_ids without specifying either "
                "asset_contract_address or asset_contract_addresses."
            )

    def _validate_order_direction(self):
        if self.order_direction is None:
            return

        if self.order_direction not in ['asc', 'desc']:
            raise ValueError(
                f"order_direction param value ({self.order_direction}) is invalid. "
                f"Must be either 'asc' or 'desc', case sensitive."
            )

    def _validate_order_by(self) -> None:
        if self.order_by is None:
            return

        if self.order_by not in (_AssetsOrderBy.TOKEN_ID, _AssetsOrderBy.SALE_COUNT, _AssetsOrderBy.SALE_DATE, _AssetsOrderBy.SALE_PRICE, _AssetsOrderBy.VISITOR_COUNT):
            raise ValueError(
                f"order_by param value ({self.order_by}) is invalid. "
                f"Must be a value from {_AssetsOrderBy.list()}, case sensitive."
            )

    def _validate_limit(self):
        if not isinstance(self.limit, int) or not 0 <= self.limit <= 50:
            raise ValueError(f"limit param must be an int between 0 and 50.")