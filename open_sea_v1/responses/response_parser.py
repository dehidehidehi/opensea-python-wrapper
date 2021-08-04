import json
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Optional, Any

from open_sea_v1.responses.response_abc import _OpenSeaResponse


@dataclass
class _ResponseParser:
    """
    Interface for saving and loading OpenseaAPI responses from and to JSON files.
    """
    destination: Path
    response_type: Type[_OpenSeaResponse]

    def __post_init__(self):
        if not self.destination.exists():
            self.destination.parent.mkdir(parents=True)

    def dump(self, to_parse: Optional[list[list[_OpenSeaResponse]]]) -> None:
        only_original_jsons = self._recreate_original_parsed_json_response(to_parse)
        with open(str(self.destination), 'w') as f:
            json.dump(only_original_jsons, f)

    def load(self) -> Any:
        with open(str(self.destination), 'r') as f:
            parsed_json = json.load(f)
        return [[self.response_type(response) for response in collection_] for collection_ in parsed_json]

    @staticmethod
    def _recreate_original_parsed_json_response(to_parse):
        return [[event._json for event in token_id_resp] for token_id_resp in to_parse]