import requests
import time

from bdd import bddio

base_url = "https://api.boot.dev/v1/lessons"


def should_refresh_token(last_refresh: int) -> bool:
    # Refresh if it has been more than 55 minutes since the last refresh.
    # 55 minutes mimics the boot.dev CLI code
    seconds_since_refresh = int(time.time()) - last_refresh

    print(f"{int(seconds_since_refresh / 60)} minutes since refresh")

    return seconds_since_refresh > 55 * 60


def require_auth(unauthd_func):
    def authd_func(*args, **kwargs):
        bootdev_cli_config = bddio.load_bootdev_cli_config()

        # If no or invalid tokens, raise
        try:
            access_token = bootdev_cli_config["access_token"]
        except KeyError:
            raise bddio.BootdevCliConfigError("Access token not found")

        if access_token == "":
            # TODO: actually validate the format of the jwt
            raise bddio.BootdevCliConfigError("Invalid access token")

        try:
            refresh_token = bootdev_cli_config["refresh_token"]
        except KeyError:
            raise bddio.BootdevCliConfigError("Refresh token not found")

        if refresh_token == "":
            # This isnt' a great validation, but it's something
            raise bddio.BootdevCliConfigError("Invalid refresh token")

        # If refresh token is expired, refresh
        last_refresh = bootdev_cli_config.get("last_refresh", 0)

        if should_refresh_token(last_refresh):
            # TODO: config form should be validated somewhere
            api_url = bootdev_cli_config["api_url"]

            refreshed = fetch_refreshed_token(
                api_url=api_url, refresh_token=refresh_token
            )
            new_config = {
                "last_refresh": int(time.time()),
                "refresh_token": refreshed["refresh_token"],
                "access_token": refreshed["access_token"],
            }

            bddio.upsert_bootdev_cli_config(new_config)

            refresh_token = new_config["refresh_token"]
            access_token = new_config["access_token"]
            last_refresh = new_config["last_refresh"]

        # Else pass the token
        return unauthd_func(*args, **kwargs, token=access_token)

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
