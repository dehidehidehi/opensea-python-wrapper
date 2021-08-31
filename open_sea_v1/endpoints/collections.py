from dataclasses import dataclass
from typing import Optional

from open_sea_v1.endpoints.abc import BaseEndpoint
from open_sea_v1.endpoints.client import BaseClient, ClientParams
from open_sea_v1.endpoints.urls import EndpointURLS
from open_sea_v1.responses.collection import CollectionResponse


@dataclass
class CollectionsEndpoint(BaseClient, BaseEndpoint):
    """
    From OpenSea documentation:
    ----------
    Use this endpoint to fetch collections and dapps that OpenSea shows on opensea.io,
    along with dapps and smart contracts that a particular user cares about.

    Maintainer observations:
    ----------
    You cannot specify the collection name for the data you wish to retrieve.
    The only way to retrieve such data, is by getting ALL collections from OpenSea, then
    iterating over them.


    Parameters
    ----------
    client_params:
        ClientParams instance.

    asset_owner: Optional[str]
        A wallet address. If specified, will return collections where the owner
        owns at least one asset belonging to smart contracts in the collection.
        The number of assets the account owns is shown as owned_asset_count for
        each collection.

    :return: Parsed JSON
    """

    client_params: ClientParams = None
    asset_owner: Optional[str] = None

    def __post_init__(self):
        self._validate_request_params()

    @property
    def url(self):
        return EndpointURLS.COLLECTIONS.value

    @property
    def parsed_http_response(self) -> list[CollectionResponse]:
        return self.parse_http_response(CollectionResponse, 'collections')

    def _get_request(self, **kwargs):
        params = dict(
            asset_owner=self.asset_owner,
            offset=self.client_params.offset,
            limit=self.client_params.limit,
        )
        get_request_kwargs = dict(params=params)
        self._http_response = super()._get_request(**get_request_kwargs)
        return self._http_response

    def _validate_request_params(self) -> None:
        if self.asset_owner is not None and not isinstance(self.asset_owner, str):
            raise TypeError(f'{self.asset_owner=} must be a str instance representing a wallet address.')