import click
import os

from bdd import bddio
from bdd import client
from bdd.lesson import Lesson, LessonParsingError


@click.group()
def cli():
    pass


@cli.command(name="init")
def bdd_init():
    # TODO: If the user has a config, prompt for confirmation
    click.echo("Welcome to the bdd initialization process. Let's get you started.")

    # Get the boot.dev CLI path
    boot_dev_cli_config_path: str | None = None

    while boot_dev_cli_config_path is None:
        try:
            unverified_path = click.prompt(
                "Path to boot.dev configuration", "~/.bootdev.yaml"
            )
            bddio.load_yaml(os.path.expandvars(unverified_path))
            boot_dev_cli_config_path = unverified_path
            click.echo("...path verified")
        except FileNotFoundError:
            click.echo("Invalid path")

    # Get the editor command
    editor_command = click.prompt("Editor command", "nvim -p")

    # Save the config
    # TODO: keys shouldn't be strewn here
    new_config = {
        "boot_dev_cli_config_path": boot_dev_cli_config_path,
        "editor_command": editor_command,
    }

    bddio.write_config(new_config)
    click.echo(
        f"Congrats, you're all set up. You can edit your config at {bddio.CONFIG_PATH}."
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

    # TODO: move this
    editor_command = bddio.load_config()["editor_command"]
    lesson_paths = " ".join(str(p) for p in lesson.file_paths)
    os.system(f"{editor_command} {lesson_paths}")


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
