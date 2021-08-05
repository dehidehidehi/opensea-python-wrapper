import json
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Optional, Any, Union

from open_sea_v1.responses import OpenSeaResponse


@dataclass
class ResponseParser:
    """
    Interface for saving and loading OpenseaAPI responses from and to JSON files.
    """
    destination: Path
    response_type: Type[OpenSeaResponse]

    def __post_init__(self):
        if not self.destination.exists():
            self.destination.parent.mkdir(parents=True, exist_ok=True)

    def dump(self, to_parse: Optional[Union[OpenSeaResponse, list[OpenSeaResponse]]]) -> None:
        if isinstance(to_parse, list):
            the_jsons = [e._json for e in to_parse]
        else:
            the_jsons = to_parse._json
        with open(str(self.destination), 'w') as f:
            json.dump(the_jsons, f)

    def load(self) -> Any:
        with open(str(self.destination), 'r') as f:
            parsed_json = json.load(f)
        return [self.response_type(collection) for collection in parsed_json]
