import json
import os
from pathlib import Path
from typing import Any

import yaml


BASE_PATH = "~/.bdd"


def to_bdd_path(local_path: str) -> Path:
    return Path(os.path.expanduser(BASE_PATH), local_path)


CONFIG_PATH = str(to_bdd_path("bdd_config.json"))


def make_parent_dirs(path: str) -> None:
    output_file = Path(path)
    output_file.parent.mkdir(exist_ok=True, parents=True)


def check_for_config(path: str = CONFIG_PATH) -> bool:
    return os.path.isfile(path)


def _write(contents: dict | str, path: str) -> None:
    make_parent_dirs(path)
    with open(path, "w") as f:
        if isinstance(contents, dict):
            json.dump(contents, f)
        else:
            f.write(contents)


# General purpose writer that places the local path in the right directory
def write_data(contents: dict | str, local_path: str) -> None:
    _write(contents, str(to_bdd_path(local_path)))


def write_config(new_config: dict[str, str]) -> None:
    _write(new_config, CONFIG_PATH)


def load_json(path: str) -> dict[str, str]:
    with open(path) as f:
        return json.load(f)


def load_config() -> dict[str, str]:
    return load_json(CONFIG_PATH)


def load_yaml(path: str) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def load_bootdev_cli_config() -> dict[str, Any]:
    path = os.path.expanduser(load_config()["boot_dev_cli_config_path"])
    return load_yaml(path)


def write_bootdev_cli_config(full_config: dict[str, Any]):
    path = os.path.expanduser(load_config()["boot_dev_cli_config_path"])
    with open(path, "w") as f:
        yaml.dump(full_config, f)


def upsert_bootdev_cli_config(new_config: dict[str, Any]) -> dict[str, Any]:
    # Note this doesn't automatically merge partially-specified nested updates
    old_config = load_bootdev_cli_config()
    to_save = {**old_config, **new_config}

    write_bootdev_cli_config(to_save)
    return to_save


class BootdevCliConfigError(Exception):
    pass
