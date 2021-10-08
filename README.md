# OpenSea Python API Wrapper

A convenient package for interacting with the OpenSea API; which allows for asynchronous retrieval of asset data from the OpenSea marketplace (https://opensea.io/).

# Installation requires

- Python 3.9 or greater (https://www.python.org/downloads/source/)
- Packages specified in: requirements.txt

# Installation

```console
  git clone https://github.com/dehidehidehi/opensea-python-wrapper.git
 ```
```console
  cd opensea-python-wrapper
  python setup.py install
 ```

# Warning about the dev branch

- Do not expect the dev branch to be stable or complete.
- There is no documentation yet. To get a sense on how the package works, have a look at the endpoint classes in the open_sea_v1 folder. You'll probably want to instanciate an endpoint class, and call it's methods.
- There will be non backwards-compatible pushes and commit squashes on the dev branch.

# Example usage
Fetching all successful sales using the EventsEndpoint. 
Check the class for more info on additional filtering parameters.

```console
from datetime import datetime, timedelta
from open_sea_v1.endpoints.client import ClientParams
from open_sea_v1.endpoints.events import EventType, AuctionType, EventsEndpoint


asset_contract_address: str = "example_contract_string_to_replace"
after = datetime.now() - timedelta(days=5)
client_params = ClientParams()

endpoint = EventsEndpoint(
    client_params=client_params,
    asset_contract_address=asset_contract_address,
    occurred_before=None,
    occurred_after=after,
    event_type=EventType.SUCCESSFUL,
)

flattened_events_pages: list = endpoint.get_parsed_pages()
unflattened_events_pages: list[list] = endpoint.get_parsed_pages(flat=False)
```

# About the documentation

- OpenSea API V1 Documentation: https://docs.opensea.io/reference/
- Anonymous API usage is limited to 2 queries per second.

# API Key
Request an API key here: https://docs.opensea.io/reference/request-an-api-key

If you have an API key:
- Requests are automatically throttled to 20 queries per second.
- The package will automatically use the system variable OPENSEA_API_KEY as the API key.
  ```console
    export OPENSEA_API_KEY="<YOUR API KEY>"
  ```
  If this system variable is not found, you must pass the API key in the ClientParam instance for each Endpoint instance.
