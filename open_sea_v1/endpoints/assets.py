from dataclasses import dataclass
from enum import Enum
from typing import Optional

from open_sea_v1.endpoints.abc import BaseEndpoint
from open_sea_v1.endpoints.client import BaseClient, ClientParams
from open_sea_v1.endpoints.urls import EndpointURLS
from open_sea_v1.responses.asset import AssetResponse


class AssetsOrderBy(str, Enum):
    """
    Helper Enum for remembering the possible values for the order_by param of the AssetsEndpoint class.
    """
    SALE_DATE = "sale_date"
    SALE_COUNT = "sale_count"
    VISITOR_COUNT = "visitor_count"
    SALE_PRICE = "sale_price"

    @classmethod
    def list(cls) -> list[str]:
        """Returns list of values of each attribute of this String Enum."""
        return list(map(lambda c: c.value, cls))


@dataclass
class AssetsEndpoint(BaseClient, BaseEndpoint):
    """
    Opensea API Assets Endpoint.

    Parameters
    ----------
    client_params:
        Common endpoint params.

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

    collection:
        Limit responses to members of a collection. Case sensitive and must match the collection slug exactly. Will return all assets from all contracts in a collection.

    :return: Parsed JSON
    """
    client_params: ClientParams = None
    asset_contract_address: Optional[str] = None
    asset_contract_addresses: Optional[list[str]] = None
    token_ids: Optional[list[int]] = None
    collection: Optional[str] = None
    owner: Optional[str] = None
    order_by: Optional[AssetsOrderBy] = None
    order_direction: str = None
    _response_type = AssetResponse
    _json_resp_key = 'assets'

    def __post_init__(self):
        self._validate_request_params()
        if not self.client_params:
            raise AttributeError('Attribute client_params is missing.')

    @property
    def url(self):
        return EndpointURLS.ASSETS.value

    @property
    def get_params(self) -> dict:
        return dict(
            owner=self.owner,
            token_ids=self.token_ids,
            asset_contract_address=self.asset_contract_address,
            asset_contract_addresses=self.asset_contract_addresses,
            collection=self.collection,
            order_by=self.order_by,
            order_direction=self.order_direction,
            offset=self.client_params.offset,
            limit=self.client_params.limit,
        )

    @property
    def parsed_http_response(self) -> list[AssetResponse]:
        return self._parse_json_resp()  # type: ignore

    def _validate_request_params(self) -> None:
        self._validate_mandatory_params()
        self._validate_asset_contract_addresses()
        self._validate_order_direction()
        self._validate_order_by()
        self._validate_limit()

    def _validate_mandatory_params(self):
        mandatory = self.owner, self.token_ids, self.asset_contract_address, self.asset_contract_addresses, self.collection
        if all((a is None for a in mandatory)):
            raise ValueError("At least one of the following parameters must not be None:\n"
                             "owner, token_ids, asset_contract_address, asset_contract_addresses, collection")

    def _validate_asset_contract_addresses(self):
        if self.asset_contract_address and self.asset_contract_addresses:
            raise ValueError(
                "You cannot simultaneously _get_request for a single contract_address and a list of contract_addresses."
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

        if self.order_by not in AssetsOrderBy.list():
            raise ValueError(
                f"order_by param value ({self.order_by}) is invalid. "
                f"Must be a value from {AssetsOrderBy.list()}, case sensitive."
            )

    def _validate_limit(self):
        if self.client_params.limit is None:
            return
        if not isinstance(self.client_params.limit, int):
            raise TypeError("limit client param must be an int")
        if not 0 <= self.client_params.limit <= 50:
            raise ValueError(f"limit param must be an int between 0 and 50.")