from enum import Enum

OPENSEA_API_V1 = "https://api.opensea.io/api/v1/"
OPENSEA_LISTINGS_V1 = "https://api.opensea.io/wyvern/v1/"


class OpenseaApiEndpoints(str, Enum):
    ASSET = OPENSEA_API_V1 + "asset"
    ASSETS = OPENSEA_API_V1 + "assets"
    ASSET_CONTRACT = OPENSEA_API_V1 + "asset_contract"
    BUNDLES = OPENSEA_API_V1 + "bundles"
    EVENTS = OPENSEA_API_V1 + "events"
    COLLECTIONS = OPENSEA_API_V1 + "collections"
    LISTINGS = OPENSEA_LISTINGS_V1 + "orders"