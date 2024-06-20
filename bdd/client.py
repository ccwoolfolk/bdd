import requests
import time

from bddconfig import BddConfig
from bootdevcliconfig import BootdevCliConfig, BootdevCliConfigError

LESSON_PATH = "/v1/lessons"
REFRESH_PATH = "/v1/auth/refresh"


def should_refresh_token(last_refresh: int) -> bool:
    # Refresh if it has been more than 55 minutes since the last refresh.
    # 55 minutes mimics the boot.dev CLI code
    seconds_since_refresh = int(time.time()) - last_refresh

    return seconds_since_refresh > 55 * 60


def with_bootdev_cli_config(unwrapped):
    path = BddConfig().expanded_bootdev_cli_config_path
    bootdev_cli_config = BootdevCliConfig(path)

    def wrapped(*args, **kwargs):
        return unwrapped(*args, **kwargs, bootdev_cli_config=bootdev_cli_config)

    return wrapped


def require_auth(unauthd_func):
    def authd_func(*args, bootdev_cli_config, **kwargs):

        access_token = bootdev_cli_config.access_token
        refresh_token = bootdev_cli_config.refresh_token
        last_refresh = bootdev_cli_config.last_refresh

        if should_refresh_token(last_refresh):
            api_url = bootdev_cli_config.api_url

            refreshed = fetch_refreshed_token(
                api_url=api_url, refresh_token=refresh_token
            )

            bootdev_cli_config.last_refresh = int(time.time())
            bootdev_cli_config.refresh_token = refreshed["refresh_token"]
            bootdev_cli_config.access_token = refreshed["access_token"]
            bootdev_cli_config.save()

        return unauthd_func(
            *args,
            **kwargs,
            token=bootdev_cli_config.access_token,
            bootdev_cli_config=bootdev_cli_config,
        )

    return authd_func


def create_headers(token: str) -> dict[str, str]:
    return {
        "authorization": f"Bearer {token}",
        "cache-control": "no-cache",
        "origin": "null",
    }


def fetch_refreshed_token(api_url: str, refresh_token: str):
    headers = {"X-Refresh-Token": refresh_token}

    res = requests.post(f"{api_url}{REFRESH_PATH}", headers=headers)
    res.raise_for_status()

    return res.json()


@with_bootdev_cli_config
@require_auth
def fetch_lesson_contents(
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    if token is None:
        raise BddClientAuthError(
            "An access token was not provided while attempting to fetch content."
        )
    if bootdev_cli_config is None:
        raise BddClientAuthError(
            "The Bootdev CLI config was not provided while attempting to fetch content."
        )

    headers = create_headers(token)

    url = f"{bootdev_cli_config.api_url}{LESSON_PATH}/{lesson_uuid}"
    req = requests.get(url, headers=headers)

    if req.status_code in (401, 403):
        raise BddClientAuthError(
            f"Received status code {req.status_code} while fetching content."
        )

    return req.json()


class BddClientAuthError(Exception):
    pass
