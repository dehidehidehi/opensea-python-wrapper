from enum import Enum

OPENSEA_API_V1 = "https://api.opensea.io/api/v1/"
OPENSEA_LISTINGS_V1 = "https://api.opensea.io/wyvern/v1/"


class ExtendedStrEnum(str, Enum):

    @classmethod
    def list(cls) -> list[str]:
        return list(map(lambda c: c.value, cls))


class OpenseaApiEndpoints(ExtendedStrEnum):
    ASSET = OPENSEA_API_V1 + "asset"
    ASSETS = OPENSEA_API_V1 + "assets"
    ASSET_CONTRACT = OPENSEA_API_V1 + "asset_contract"
    BUNDLES = OPENSEA_API_V1 + "bundles"
    EVENTS = OPENSEA_API_V1 + "events"
    COLLECTIONS = OPENSEA_API_V1 + "collections"
    LISTINGS = OPENSEA_LISTINGS_V1 + "orders"


class AssetsOrderBy(ExtendedStrEnum):
    TOKEN_ID = "token_id"
    SALE_DATE = "sale_date"
    SALE_COUNT = "sale_count"
    VISITOR_COUNT = "visitor_count"
    SALE_PRICE = "sale_price"


class Asset(ExtendedStrEnum):
    TOKEN_ID = "token_id"
    NUM_SALES = "num_sales"
    BACKGROUND_COLOR = "background_color"
    IMAGE_URL = "image_url"
    IMAGE_PREVIEW_URL = "image_preview_url"
    IMAGE_THUMBNAIL_URL = "image_thumbnail_url"
    IMAGE_ORIGINAL_URL = "image_original_url"
    ANIMATION_URL = "animation_url"
    ANIMATION_ORIGINAL_URL = "animation_original_url"
    NAME = "name"
    DESCRIPTION = "description"
    EXTERNAL_LINK = "external_link"
    ASSET_CONTRACT_DICT = "asset_contract"
    PERMALINK = "permalink"
    COLLECTION_DICT = "collection"
    DECIMALS = "decimals"
    TOKEN_METADATA = "token_metadata"
    OWNER_DICT = "owner"
    SELL_ORDERS = "sell_orders"
    CREATOR_DICT = "creator"
    TRAITS_DICT = "traits"
    LAST_SALE_DICT = "last_sale"
    TOP_BID = "top_bid"
    LISTING_DATE = "listing_date"
    IS_PRESALE = "is_presale"
    TRANSFER_FEE_PAYMENT_TOKEN = "transfer_fee_payment_token"
    TRANSFER_FEE = "transfer_fee"


class AssetTraits(ExtendedStrEnum):
    TRAIT_TYPE = "trait_type"
    VALUE = "value"
    DISPLAY_TYPE = "display_type"


class AssetContract(ExtendedStrEnum):
    ADDRESS = "address"
    NAME = "name"
    SYMBOL = "symbol"
    IMAGE_URL = "image_url"
    DESCRIPTION = "description"
    EXTERNAL_LINK = "external_link"


class AssetOwner(ExtendedStrEnum):
    ADDRESS = 'address'
    CONFIG = 'config'
    PROFILE_IMG_URL = 'profile_img_url'
    USER = 'user'


class AssetLastSale(ExtendedStrEnum):
    ASSET = 'asset'
    ASSET_BUNDLE = 'asset_bundle'
    EVENT_TYPE = 'event_type'
    EVENT_TIMESTAMP = 'event_timestamp'
    AUCTION_TYPE = 'auction_type'
    TOTAL_PRICE = 'total_price'
    PAYMENT_TOKEN_DICT = 'payment_token'
    TRANSACTION_DICT = 'transaction'
    CREATED_DATE = 'created_date'
    QUANTITY = 'quantity'