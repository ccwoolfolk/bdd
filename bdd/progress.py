from typing import Callable
from bdd.client import fetch_course_progress
from .bddio import read_data, write_data

PROGRESS_FILE = "progress.json"


# TODO: store names and chapter/course to display on moves


def get_current_lesson_uuid() -> str | None:
    return _read_progress().get("current")


def move_to(lesson_uuid: str):
    prev_uuid, next_uuid = _find_prev_and_next(lesson_uuid)
    _save_progress(lesson_uuid, prev_uuid, next_uuid)


def move_to_next() -> str:
    return _move_to_prev_or_next(_get_next_lesson_uuid)


def move_to_prev() -> str:
    return _move_to_prev_or_next(_get_prev_lesson_uuid)


def _move_to_prev_or_next(uuid_getter: Callable) -> str:
    uuid = uuid_getter()
    if uuid is None:
        current_uuid = get_current_lesson_uuid()
        if current_uuid is None:
            raise NoLastActiveLessonError()
        raise LessonDoesNotExistError()
    move_to(uuid)
    return uuid


def _get_next_lesson_uuid() -> str | None:
    return _read_progress().get("next")


def _get_prev_lesson_uuid() -> str | None:
    return _read_progress().get("prev")


def _save_progress(
    current_uuid: str, prev_uuid: str | None = None, next_uuid: str | None = None
):
    progress = {
        "current": current_uuid,
        "prev": prev_uuid,
        "next": next_uuid,
    }
    write_data(progress, PROGRESS_FILE)


def _read_progress() -> dict[str, str | None]:
    try:
        return read_data(PROGRESS_FILE)
    except FileNotFoundError:
        raise NoLastActiveLessonError()


def _find_prev_and_next(lesson_uuid: str) -> tuple[str | None, str | None]:
    payload = fetch_course_progress(lesson_uuid)
    course_uuid = payload["CourseUUID"]

    chapters = payload["Chapters"]
    for chapter in chapters:
        lessons = chapter["Lessons"]
        for lesson_i, lesson in enumerate(lessons):
            if lesson["UUID"] == lesson_uuid:
                chapter_uuid = chapter["UUID"]
                prev_uuid = None
                next_uuid = None

                # TODO: this needs to handle changing chapters
                if lesson_i > 0:
                    prev_uuid = lessons[lesson_i - 1]["UUID"]
                if lesson_i < len(lessons) - 1:
                    next_uuid = lessons[lesson_i + 1]["UUID"]

                return prev_uuid, next_uuid
    return None, None


class ProgressError(Exception):
    pass


class NoLastActiveLessonError(ProgressError):
    pass


class LessonDoesNotExistError(ProgressError):
    pass
