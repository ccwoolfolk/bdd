from typing import Callable
import os

from . import client
from . import progress
from .lesson import Lesson, LessonParsingError, LessonType, ProgLang
from .bddconfig import BddConfig


class CommandError(Exception):
    pass


def initialize_bdd(
    get_boot_dev_cli_config_path: Callable[[BddConfig], str],
    get_editor_command: Callable[[BddConfig], str],
) -> BddConfig:
    bdd_config = BddConfig(use_defaults=True)
    bdd_config.boot_dev_cli_config_path.value = get_boot_dev_cli_config_path(bdd_config)
    bdd_config.editor_command.value = get_editor_command(bdd_config)
    bdd_config.save()
    return bdd_config


def get_lesson(url: str | None) -> Lesson:
    # TODO: check if files already exist to avoid clobbering existing work
    # TODO: move this
    if url is not None:
        split_url = url.split("/lessons/")
        assert len(split_url) == 2
        uuid = split_url[1]
        assert "/" not in uuid
    else:
        uuid = progress.get_current_lesson_uuid()

    contents = client.fetch_lesson_contents(uuid)

    try:
        lesson = Lesson.from_api_payload(contents)
    except LessonParsingError as e:
        raise CommandError(f"Unable to parse your lesson: {e}")

    lesson.save()
    progress.move_to(uuid)

    if not lesson.is_supported_lesson_type:
        raise CommandError(
            "Uh oh, this is not a supported lesson type! You'll need to complete this lesson without bdd."
        )

    return lesson


def open_lesson(lesson: Lesson):
    editor_command = BddConfig().editor_command.value
    lesson_paths = " ".join(str(p) for p in lesson.file_paths)
    os.system(f"{editor_command} {lesson_paths}")


def run_lesson():
    uuid = progress.get_current_lesson_uuid()
    lesson = Lesson.from_disk(uuid)

    match lesson.lesson_type:
        case LessonType.CODE_TESTS:
            raise NotImplementedError()
        case LessonType.CLI_COMMAND | LessonType.HTTP_TESTS:
            # We are Very Smart so we pass the work to the bootdev cli
            os.system(f"bootdev run {uuid}")
        case LessonType.CHOICE:
            raise CommandError(
                "Multiple choice lessons don't support `run`. You can `submit` directly."
            )
        case _:
            raise NotImplementedError()


def submit_lesson(submission: str | None):
    uuid = progress.get_current_lesson_uuid()
    lesson = Lesson.from_disk(uuid)

    match lesson.lesson_type:
        case LessonType.CODE_TESTS:
            raise NotImplementedError()
        case LessonType.CLI_COMMAND | LessonType.HTTP_TESTS:
            # We are Very Smart so we pass the work to the bootdev cli
            os.system(f"bootdev submit {uuid}")
        case LessonType.CHOICE:
            if submission is None or submission == "":
                raise CommandError(
                    'This is a multiple choice lesson. Submit like: `bdd submit "My answer here"`'
                )
            client.submit_multiple_choice(submission, uuid)
        case _:
            raise NotImplementedError()


def go_to_next() -> str:
    try:
        uuid = progress.move_to_next()
    except progress.NoLastActiveLessonError:
        raise CommandError(
            "There is no last active lesson saved. Try first retrieving a lesson directly via the URL before using the next and prev functionality."
        )
    except progress.LessonDoesNotExistError:
        raise CommandError(
            "There is no next lesson. Congrats on completing the course."
        )

    return uuid


def go_to_prev() -> str:
    try:
        uuid = progress.move_to_prev()
    except progress.NoLastActiveLessonError:
        raise CommandError(
            "There is no last active lesson saved. Try first retrieving a lesson directly via the URL before using the next and prev functionality."
        )
    except progress.LessonDoesNotExistError:
        raise CommandError("There is no previous lesson.")

    return uuid
