from pathlib import Path
import tempfile
import json
from typing import List, Dict, Union


def read_json(path: Path) -> Union[Dict, List[Dict]]:
    with open(path) as f:
        j = json.load(f)
    return j


def write_json(json_data: Union[Dict, List[Dict]], path: Path, prettify: bool = True) -> None:
    with open(path, "w") as f:
        if prettify:
            json.dump(json_data, f, indent=4)
        else:
            json.dump(json_data, f)


def create_empty_temp_file(prefix=None, suffix=None) -> Path:
    _, path = tempfile.mkstemp(prefix=prefix, suffix=suffix, text=True)
    return Path(path)
