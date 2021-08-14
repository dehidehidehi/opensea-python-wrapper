import json
from dataclasses import dataclass
from pathlib import Path
from typing import Type, Optional, Any, Union

from open_sea_v1.responses.abc import BaseResponse


@dataclass
class ResponseParser:
    """
    Interface for saving and loading OpenseaAPI responses from and to JSON files.
    """
    destination: Path
    response_type: Type[BaseResponse]

    def __post_init__(self):
        if not self.destination.exists():
            self.destination.parent.mkdir(parents=True, exist_ok=True)

    def dump(self, to_parse: Optional[Union[BaseResponse, list[BaseResponse]]]) -> None:
        if isinstance(to_parse, list):
            the_jsons = [e._json for e in to_parse]
        else:
            the_jsons = to_parse._json
        with open(str(self.destination), 'w') as f:
            json.dump(the_jsons, f)

    def load(self, json_path: Optional[Path] = None) -> Any:
        json_path = self.destination if not json_path else json_path
        with open(str(json_path), 'r') as f:
            parsed_json = json.load(f)
        return [self.response_type(collection) for collection in parsed_json]

    def load_from_dir(self) -> Any:
        detected_json_files = (p for p in self.destination.iterdir() if '.json' in p.name and not p.is_dir())
        return [self.load(json_path) for json_path in detected_json_files]
