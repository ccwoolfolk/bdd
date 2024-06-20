import click
import os

from bdd import client
from .bddio import load_yaml, to_bdd_path
from .lesson import Lesson, LessonParsingError
from .bddconfig import BddConfig


@click.group()
def cli():
    pass


@cli.command(name="init")
def bdd_init():
    # TODO: If the user has a config, prompt for confirmation
    click.echo("Welcome to the bdd initialization process. Let's get you started.")
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
        click.echo(
            click.style(
                "Uh oh, this is not a supported lesson type! You'll need to complete this lesson without bdd.",
                fg="red",
            )
        )


@cli.command(name="run")
@click.argument("uuid", required=False)
def bdd_run():
    click.echo("run stub")


@cli.command(name="submit")
@click.argument("uuid", required=False)
def bdd_submit():
    click.echo("submit stub")


@cli.command(name="next")
@click.argument("uuid", required=False)
def bdd_next():
    click.echo("next stub")


@cli.command(name="prev")
@click.argument("uuid", required=False)
def bdd_prev():
    click.echo("prev stub")
