from requests import Response, request


class OpenSeaClient:

    api_key = None

    @property
    def http_headers(self) -> dict:
        return {
            "headers":
                {"X-API-Key" : self.api_key} if self.api_key else dict(),
        }

    def get_request(self, url: str, method: str = 'GET', **kwargs) -> Response:
        """
        Automatically passes in API key in HTTP get_request headers.
        """
        if 'api_key' in kwargs:
            self.api_key = kwargs.pop('api_key')
        updated_kwargs = kwargs | self.http_headers
        return request(method, url, **updated_kwargs)

    # def collections(self, *, asset_owner: Optional[str] = None, offset: int, limit: int) -> OpenseaCollections:
    #     """
    #     Use this endpoint to fetch collections and dapps that OpenSea shows on opensea.io,
    #     along with dapps and smart contracts that a particular user cares about.
    #
    #     :param asset_owner: A wallet address. If specified, will return collections where
    #      the owner owns at least one asset belonging to smart contracts in the collection.
    #       The number of assets the account owns is shown as owned_asset_count for each collection.
    #     :param offset: For pagination. Number of contracts offset from the beginning of the result list.
    #     :param limit: For pagination. Maximum number of contracts to return.
    #     :return: Parsed JSON
    #     """
    #     if offset != 0:
    #         raise NotImplementedError(
    #             "Sorry, tested offset parameter is not implemented yet. "
    #             "Feel free to PR after looking at the tests and trying to understand"
    #             " why current implementation doesn't allow pagination to work..."
    #         )
    #     resp = self._collections(asset_owner=asset_owner, offset=offset, limit=limit)
    #     return resp.json()['collections']
    #
    # def _collections(self, **_request_params) -> Response:
    #     """Returns HTTPResponse object."""
    #     url = OpenseaApiEndpoints.COLLECTIONS.value
    #     return self.get_request("GET", url, _request_params=_request_params)
    #
    # def asset(self, asset_contract_address: str, token_id: str, account_address: Optional[str] = None) -> OpenseaAsset:
    #     """
    #     :param asset_contract_address: Address of the contract for this NFT
    #     :param token_id: Token ID for this item
    #     :param account_address: Address of an owner of the token. If you include this, the http_response will include an ownership object that includes the number of tokens owned by the address provided instead of the top_ownerships object included in the standard http_response, which provides the number of tokens owned by each of the 10 addresses with the greatest supply of the token.
    #     :return: Parsed JSON.
    #     """
    #     resp = self._asset(
    #         asset_contract_address=asset_contract_address,
    #         token_id=token_id,
    #         account_address=account_address,
    #     )
    #     return resp.response()

