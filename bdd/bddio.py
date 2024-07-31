import json
import os
from pathlib import Path
from typing import Any

import yaml


BASE_PATH = "~/.bdd"


def check_exists(path: str | Path) -> bool:
    return os.path.exists(path)


def to_bdd_path(local_path: str) -> Path:
    return Path(os.path.expanduser(BASE_PATH), local_path)


def make_parent_dirs(path: str) -> None:
    output_file = Path(path)
    output_file.parent.mkdir(exist_ok=True, parents=True)


def _write(contents: dict | str, path: str) -> None:
    make_parent_dirs(path)
    with open(path, "w") as f:
        if isinstance(contents, dict):
            json.dump(contents, f)
        else:
            f.write(contents)


# General purpose reader that prepends the local path with the right directory
def read_data(local_path: str) -> dict[str, Any] | str:
    path = Path(to_bdd_path(local_path))

    match path.suffix:
        case ".json":
            return load_json(str(path))
        case ".yaml":
            return load_yaml(str(path))
        case ".md" | ".txt":
            return load_text(str(path))
        case _:
            raise ValueError()


# General purpose writer that places the local path in the right directory
def write_data(contents: dict | str, local_path: str) -> None:
    _write(contents, str(to_bdd_path(local_path)))


def load_json(path: str) -> dict[str, str]:
    with open(path) as f:
        return json.load(f)


def load_text(path: str) -> str:
    with open(path) as f:
        return f.read()


def load_yaml(path: str) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def write_yaml(contents: dict, path: str):
    with open(path, "w") as f:
        yaml.dump(contents, f)
