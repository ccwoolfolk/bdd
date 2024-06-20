from typing import Any

from .bddio import load_yaml, write_yaml


# We only expose the necessary fields here
class BootdevCliConfig:
    def __init__(self, path: str):
        self.__path = path
        self.__config = load_yaml(self.__path)
        BootdevCliConfig._prevalidate_access_token(self.access_token)
        BootdevCliConfig._prevalidate_refresh_token(self.refresh_token)
        BootdevCliConfig._prevalidate_last_refresh(self.last_refresh)

    @property
    def access_token(self) -> str:
        return self._access_config_key("access_token")

    @access_token.setter
    def access_token(self, value: str):
        BootdevCliConfig._prevalidate_access_token(value)
        self.__config["access_token"] = value

    @property
    def refresh_token(self) -> str:
        return self._access_config_key("refresh_token")

    @refresh_token.setter
    def refresh_token(self, value: str):
        BootdevCliConfig._prevalidate_refresh_token(value)
        self.__config["refresh_token"] = value

    @property
    def last_refresh(self) -> int:
        return self._access_config_key("last_refresh")

    @last_refresh.setter
    def last_refresh(self, value: int):
        BootdevCliConfig._prevalidate_last_refresh(value)
        self.__config["last_refresh"] = value

    @property
    def api_url(self):
        return self._access_config_key("api_url")

    def save(self):
        write_yaml(self.__config, self.__path)

    def _access_config_key(self, key: str):
        try:
            return self.__config[key]
        except KeyError:
            raise BootdevCliConfigError(f"'{key}' not found.")

    @staticmethod
    def _prevalidate_last_refresh(token: Any):
        try:
            assert isinstance(token, int)
            assert token != ""
        except AssertionError:
            raise BootdevCliConfigError(f"'{token}' is not a valid refresh token.")

    @staticmethod
    def _prevalidate_refresh_token(token: Any):
        try:
            assert isinstance(token, str)
            assert token != ""
        except AssertionError:
            raise BootdevCliConfigError(f"'{token}' is not a valid refresh token.")

    @staticmethod
    def _prevalidate_access_token(token: Any):
        try:
            assert isinstance(token, str)
            assert len(token.split(".")) == 3
        except AssertionError:
            raise BootdevCliConfigError(f"'{token}' is not a valid access token.")


class BootdevCliConfigError(Exception):
    pass
