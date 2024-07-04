import requests
import time

from .bddconfig import BddConfig
from .bootdevcliconfig import BootdevCliConfig, BootdevCliConfigError

LESSON_PATH = "/v1/lessons"
PROGRESS_PATH = "/v1/course_progress_by_lesson"
REFRESH_PATH = "/v1/auth/refresh"


def should_refresh_token(last_refresh: int) -> bool:
    # Refresh if it has been more than 55 minutes since the last refresh.
    # 55 minutes mimics the boot.dev CLI code
    seconds_since_refresh = int(time.time()) - last_refresh

    return seconds_since_refresh > 55 * 60


def with_bootdev_cli_config(unwrapped):
    def wrapped(*args, **kwargs):
        path = BddConfig().expanded_bootdev_cli_config_path
        bootdev_cli_config = BootdevCliConfig(path)
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
def fetch_course_progress(
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    return _make_bdd_req(
        f"{PROGRESS_PATH}/{lesson_uuid}", token, bootdev_cli_config
    ).json()


@with_bootdev_cli_config
@require_auth
def fetch_lesson_contents(
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    return _make_bdd_req(
        f"{LESSON_PATH}/{lesson_uuid}", token, bootdev_cli_config
    ).json()


@with_bootdev_cli_config
@require_auth
def submit_manual(
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    return _make_bdd_req(
        f"{LESSON_PATH}/{lesson_uuid}/manual",
        token,
        bootdev_cli_config,
        http_method="POST",
    ).json()


@with_bootdev_cli_config
@require_auth
def submit_multiple_choice(
    answer: str,
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    return _make_bdd_req(
        f"{LESSON_PATH}/{lesson_uuid}/multiple_choice",
        token,
        bootdev_cli_config,
        http_method="POST",
        payload={"answer": answer},
    ).json()


@with_bootdev_cli_config
@require_auth
def submit_code(
    output: str,
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    return _make_bdd_req(
        f"{LESSON_PATH}/{lesson_uuid}/code",
        token,
        bootdev_cli_config,
        http_method="POST",
        payload={"output": output},
    ).json()


@with_bootdev_cli_config
@require_auth
def submit_code_tests(
    output: str,
    lesson_uuid: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
):
    return _make_bdd_req(
        f"{LESSON_PATH}/{lesson_uuid}/code_tests",
        token,
        bootdev_cli_config,
        http_method="POST",
        payload={"output": output},
    ).json()


def _make_bdd_req(
    path: str,
    token: str | None = None,
    bootdev_cli_config: BootdevCliConfig | None = None,
    http_method: str = "GET",
    payload: dict | None = None,
) -> requests.Response:
    checked_token, config = _validate_api_inputs(token, bootdev_cli_config)
    headers = create_headers(checked_token)
    url = f"{config.api_url}{path}"

    match http_method:
        case "GET":
            res = requests.get(url, headers=headers)
        case "POST":
            res = requests.post(url, headers=headers, json=payload)
        case _:
            raise BddClientError(f"Unrecognized http method: {http_method}")

    if res.status_code != requests.codes.ok:
        raise BddClientError(
            f"Received status code {res.status_code} while fetching from {url}."
        )

    return res


def _validate_api_inputs(
    token: str | None, config: BootdevCliConfig | None
) -> tuple[str, BootdevCliConfig]:
    if token is None:
        raise BddClientError(
            "An access token was not provided while attempting to fetch content."
        )
    if config is None:
        raise BddClientError(
            "The Bootdev CLI config was not provided while attempting to fetch content."
        )
    return token, config


class BddClientError(Exception):
    pass
