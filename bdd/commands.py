from typing import Callable
import click
import os

from . import client
from . import progress
from .bddio import load_yaml, to_bdd_path
from .lesson import Lesson, LessonParsingError, LessonType
from .bddconfig import BddConfig


@click.group()
def cli():
    pass


@cli.command(name="init")
def bdd_init():
    click.echo("Welcome to the bdd initialization process. Let's get you started.")

    if BddConfig.get_config_exists():
        proceed = click.confirm(
            "You already have a config file. Proceeding will overwrite your existing config. Do you want to continue?"
        )
        if proceed:
            click.echo("Ok, let's proceed.")
        else:
            click.echo("Aborting initialization process.")
            return

    bdd_config = BddConfig(use_defaults=True)

    # Get the boot.dev CLI path
    unverified_path: str | None = None
    while unverified_path is None:
        unverified_path = click.prompt(
            bdd_config.boot_dev_cli_config_path.description,
            bdd_config.boot_dev_cli_config_path.default,
        )

        try:
            load_yaml(os.path.expandvars(str(unverified_path)))
        except FileNotFoundError:
            click.echo("Invalid path")
            unverified_path = None

        bdd_config.boot_dev_cli_config_path.value = str(unverified_path)
        click.echo("...path verified")

    # Get the editor command
    bdd_config.editor_command.value = click.prompt(
        bdd_config.editor_command.description, bdd_config.editor_command.default
    )

    # Wrap up
    bdd_config.save()
    click.echo(
        f"Congrats, you're all set up. You can edit your config at {to_bdd_path(BddConfig.CONFIG_FILENAME)}."
    )
    click.echo('Try "bdd get --help" to start completing lessons locally.')


@cli.command(name="get")
@click.argument("url", required=True)
def bdd_get(url: str):
    # TODO: handle no url case now that progress tracking is available
    # TODO: check if files already exist to avoid clobbering existing work
    # TODO: move this
    split_url = url.split("/lessons/")
    assert len(split_url) == 2
    uuid = split_url[1]
    assert "/" not in uuid

    click.echo(f"Getting lesson {uuid}")
    contents = client.fetch_lesson_contents(uuid)

    try:
        lesson = Lesson.from_api_payload(contents)
    except LessonParsingError as e:
        click.echo(f"Unable to parse your lesson: {e}")
        return

    lesson.save()
    click.echo("...lesson retrieved and saved!")

    if lesson.is_supported_lesson_type:
        editor_command = BddConfig().editor_command.value
        lesson_paths = " ".join(str(p) for p in lesson.file_paths)
        os.system(f"{editor_command} {lesson_paths}")
    else:
        _print_error(
            "Uh oh, this is not a supported lesson type! You'll need to complete this lesson without bdd."
        )

    progress.move_to(uuid)


@cli.command(name="run")
def bdd_run():
    uuid = progress.get_current_lesson_uuid()
    lesson = Lesson.from_disk(uuid)

    match lesson.lesson_type:
        case LessonType.CODE_TESTS:
            raise NotImplementedError()
        case LessonType.CLI_COMMAND:
            # We are Very Smart so we pass the work to the bootdev cli
            os.system(f"bootdev run {uuid}")
        case _:
            raise NotImplementedError()


@cli.command(name="submit")
def bdd_submit():
    uuid = progress.get_current_lesson_uuid()
    lesson = Lesson.from_disk(uuid)

    match lesson.lesson_type:
        case LessonType.CODE_TESTS:
            raise NotImplementedError()
        case LessonType.CLI_COMMAND:
            # We are Very Smart so we pass the work to the bootdev cli
            os.system(f"bootdev submit {uuid}")
        case _:
            raise NotImplementedError()


@cli.command(name="next")
def bdd_next():
    try:
        uuid = progress.move_to_next()
        click.echo(f"Moved to lesson {uuid}")
    except progress.NoLastActiveLessonError:
        click.echo(
            "There is no last active lesson saved. Try first retrieving a lesson directly via the URL before using the next and prev functionality."
        )
    except progress.LessonDoesNotExistError:
        click.echo("There is no next lesson. Congrats on completing the course.")


@cli.command(name="prev")
def bdd_prev():
    try:
        uuid = progress.move_to_prev()
        click.echo(f"Moved to lesson {uuid}")
    except progress.NoLastActiveLessonError:
        click.echo(
            "There is no last active lesson saved. Try first retrieving a lesson directly via the URL before using the next and prev functionality."
        )
    except progress.LessonDoesNotExistError:
        click.echo("There is no previous lesson.")


def _print_error(msg: str):
    click.echo(
        click.style(
            msg,
            fg="red",
        )
    )
