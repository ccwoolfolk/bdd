from dataclasses import dataclass
from typing import Any, Callable
from bdd.client import fetch_course_progress
from .bddio import read_data, write_data

PROGRESS_FILE = "progress.json"


def get_current_lesson_uuid() -> str:
    uuid = _read_progress().get("current")
    if uuid is None:
        raise NoLastActiveLessonError()
    return uuid


def move_to(lesson_uuid: str):
    progress_map = fetch_course_progress(lesson_uuid)
    prev_uuid, next_uuid = find_prev_and_next(lesson_uuid, progress_map)
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
        data = read_data(PROGRESS_FILE)
        assert type(data) == dict, "Unexpected format for progress file"
        return data
    except FileNotFoundError:
        raise NoLastActiveLessonError()


def find_prev_and_next(
    lesson_uuid: str, progress_map: dict[Any, Any]
) -> tuple[str | None, str | None]:

    chapters = progress_map["Chapters"]
    for chapter_i, chapter in enumerate(chapters):
        lessons = chapter["Lessons"]
        for lesson_i, lesson in enumerate(lessons):
            if lesson["UUID"] == lesson_uuid:
                prev_uuid = None
                next_uuid = None

                if lesson_i > 0:
                    prev_uuid = lessons[lesson_i - 1]["UUID"]
                elif chapter_i > 0:
                    prev_chapter = chapters[chapter_i - 1]
                    prev_lessons = prev_chapter["Lessons"]
                    prev_uuid = prev_lessons[-1]["UUID"]

                if lesson_i < len(lessons) - 1:
                    next_uuid = lessons[lesson_i + 1]["UUID"]
                elif chapter_i < len(chapters) - 1:
                    next_chapter = chapters[chapter_i + 1]
                    next_uuid = next_chapter["Lessons"][0]["UUID"]

                return prev_uuid, next_uuid
    return None, None


@dataclass
class ChapterProgress:
    n_required_complete: int
    n_required: int
    n_optional_complete: int
    n_total: int


LessonSummary = tuple[bool, str, bool, bool]
ChapterSummary = tuple[str, bool, ChapterProgress, list[LessonSummary]]


def retrieve_course_progress(uuid: str | None) -> list[ChapterSummary]:
    current_uuid = uuid or get_current_lesson_uuid()
    payload = fetch_course_progress(current_uuid)
    return summarize_course_progress(current_uuid, lambda: payload)


def summarize_course_progress(
    active_uuid: str, get_progress: Callable[[], dict[str, Any]]
) -> list[ChapterSummary]:
    # retrieve progress
    # parse progress
    progress_map = get_progress()

    chapters: list[ChapterSummary] = []

    for chapter in progress_map["Chapters"]:
        title = chapter["Title"]
        n_required_complete = 0
        n_required = 0
        n_optional_complete = 0
        n_total = 0
        is_chapter_active = False
        lessons: list[LessonSummary] = []

        for l in chapter["Lessons"]:
            n_total += 1
            n_required_complete += int(l["IsRequired"] and l["IsComplete"])
            n_optional_complete += int(not l["IsRequired"] and l["IsComplete"])
            n_required += int(l["IsRequired"])
            is_lesson_active = l["UUID"] == active_uuid
            is_chapter_active = is_chapter_active or is_lesson_active
            lessons.append(
                (is_lesson_active, l["Title"], l["IsRequired"], l["IsComplete"])
            )

        chapter_progress = ChapterProgress(
            n_total=n_total,
            n_required_complete=n_required_complete,
            n_required=n_required,
            n_optional_complete=n_optional_complete,
        )
        chapters.append((title, is_chapter_active, chapter_progress, lessons))

    return chapters


def print_progress(
    summary: list[ChapterSummary], logger: Callable[[str], None], verbose: bool
) -> None:
    for title, is_active, progress, lessons in summary:
        if not verbose and not is_active:
            continue
        message = "* " if is_active else "  "
        message += f"{title} ({progress.n_required_complete}/{progress.n_required} required, {progress.n_optional_complete + progress.n_required_complete}/{progress.n_total} total)"
        logger(message)
        if is_active:
            for lesson in lessons:
                l_is_active, l_title, l_required, l_complete = lesson
                l_message = "  * " if l_is_active else "    "
                l_message += f"{l_title} ({'✅' if l_complete else '❌'})"
                logger(l_message)


class ProgressError(Exception):
    pass


class NoLastActiveLessonError(ProgressError):
    pass


class LessonDoesNotExistError(ProgressError):
    pass
