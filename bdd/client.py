import requests
import time

from bddconfig import BddConfig
from bootdevcliconfig import BootdevCliConfig, BootdevCliConfigError

base_url = "https://api.boot.dev/v1/lessons"


def should_refresh_token(last_refresh: int) -> bool:
    # Refresh if it has been more than 55 minutes since the last refresh.
    # 55 minutes mimics the boot.dev CLI code
    seconds_since_refresh = int(time.time()) - last_refresh

    print(f"{int(seconds_since_refresh / 60)} minutes since refresh")

    return seconds_since_refresh > 55 * 60


def require_auth(unauthd_func):
    def authd_func(*args, **kwargs):
        path = BddConfig().expanded_bootdev_cli_config_path
        bootdev_cli_config = BootdevCliConfig(path)

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

        return unauthd_func(*args, **kwargs, token=bootdev_cli_config.access_token)

    return authd_func


def create_headers(token: str) -> dict[str, str]:
    return {
        "authorization": f"Bearer {token}",
        "cache-control": "no-cache",
        "origin": "null",
    }


def fetch_refreshed_token(api_url: str, refresh_token: str):
    print("Refreshing...")

    refresh_path = "/v1/auth/refresh"
    headers = {"X-Refresh-Token": refresh_token}

    res = requests.post(f"{api_url}{refresh_path}", headers=headers)
    res.raise_for_status()

    return res.json()


@require_auth
def fetch_lesson_contents(lesson_uuid: str, token: str | None = None):
    print("Fetching...")
    if token is None:
        # TODO: pick a more specific exception
        raise Exception("Token not set")

    headers = create_headers(token)

    req = requests.get(
        f"https://api.boot.dev/v1/lessons/{lesson_uuid}", headers=headers
    )
    print(req)

    if req.status_code in (401, 403):
        # TODO: pick a more specific exception
        raise Exception("Auth error. Refresh JWT")

    return req.json()
