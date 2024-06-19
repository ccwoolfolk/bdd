from dataclasses import dataclass
from typing import Any

from bddio import read_data, write_data

@dataclass
class ConfigField:
    key: str
    value: str
    default: str
    description: str


class BddConfig:
    CONFIG_FILENAME = 'bdd_config.json'

    def __init__(self, use_defaults=False):
        # Populate with the default values first.
        # These are replaced after loading the config.
        self.boot_dev_cli_config_path = ConfigField(
            "boot_dev_cli_config_path",
            "~/.bootdev.yaml",
            "~/.bootdev.yaml",
            "Path to boot.dev configuration",
        )
        self.editor_command = ConfigField(
            "editor_command", "nvim -p", "nvim -p", "Editor command"
        )
        self.fields = [self.boot_dev_cli_config_path, self.editor_command]

        if not use_defaults:
            loaded_config = BddConfig._load_config()
            for field in self.fields:
                field.value = loaded_config[field.key]

    @staticmethod
    def _load_config() -> dict[str, str]:
        return read_data(BddConfig.CONFIG_FILENAME)

    @staticmethod
    def get_config_exists():
        try:
            BddConfig._load_config()
            return True
        except FileNotFoundError:
            return False

    def save(self):
        new_config = {
            field.key: field.value
            for field
            in self.fields
        }
        write_data(new_config, BddConfig.CONFIG_FILENAME)


# TODO: clean these up using the BddConfig pattern
def load_bootdev_cli_config() -> dict[str, Any]:
    import os
    from bddio import load_yaml

    path = os.path.expanduser(BddConfig().boot_dev_cli_config_path.value)
    return load_yaml(path)


def write_bootdev_cli_config(full_config: dict[str, Any]):
    import os
    import yaml
    path = os.path.expanduser(BddConfig().boot_dev_cli_config_path.value)
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
