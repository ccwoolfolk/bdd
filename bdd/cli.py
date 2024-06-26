import click
import os

from . import commands
from .bddio import load_yaml, to_bdd_path
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

    try:
        commands.initialize_bdd(
            _prompt_for_boot_dev_cli_config_path, _prompt_for_editor_command
        )
    except commands.CommandError as e:
        _print_error(str(e))
        return

    config_path = to_bdd_path(BddConfig.CONFIG_FILENAME)
    click.echo(
        f"Congrats, you're all set up. You can edit your config at {config_path}."
    )
    click.echo('Try "bdd get --help" to start completing lessons locally.')


@cli.command(name="get")
@click.argument("url", required=False)
def bdd_get(url: str | None):
    try:
        lesson = commands.get_lesson(url)
    except commands.CommandError as e:
        _print_error(str(e))
        return

    click.echo(f"Lesson '{lesson.uuid}' retrieved and saved!")
    commands.open_lesson(lesson)


@cli.command(name="run")
def bdd_run():
    try:
        commands.run_lesson()
    except commands.CommandError as e:
        _print_error(str(e))


@cli.command(name="submit")
@click.argument("submission", required=False)
def bdd_submit(submission: str | None):
    try:
        commands.submit_lesson(submission)
    except commands.CommandError as e:
        _print_error(str(e))


@cli.command(name="next")
def bdd_next():
    try:
        uuid = commands.go_to_next()
        click.echo(f"Moved to lesson {uuid}")
    except commands.CommandError as e:
        _print_error(str(e))


@cli.command(name="prev")
def bdd_prev():
    try:
        uuid = commands.go_to_prev()
        click.echo(f"Moved to lesson {uuid}")
    except commands.CommandError as e:
        _print_error(str(e))


def _print_error(msg: str):
    click.echo(
        click.style(
            msg,
            fg="red",
        )
    )


def _prompt_for_boot_dev_cli_config_path(bdd_config: BddConfig) -> str:
    path: str | None = None
    while path is None:
        path = click.prompt(
            bdd_config.boot_dev_cli_config_path.description,
            bdd_config.boot_dev_cli_config_path.default,
        )

        try:
            load_yaml(os.path.expandvars(str(path)))
        except FileNotFoundError:
            click.echo("Invalid path")
            path = None

    return path


def _prompt_for_editor_command(bdd_config: BddConfig) -> str:
    return click.prompt(
        bdd_config.editor_command.description, bdd_config.editor_command.default
    )
