"""Helpers for dealing with boot.dev conventions and data structures"""

import json
from typing import Any, Callable
from . import lesson


def get_lesson_uuid_from_url(url: str) -> str:
    split_url = url.split("/lessons/")
    error_message = f"Cannot parse lesson UUID from URL: {url}"
    assert len(split_url) == 2, error_message

    uuid = split_url[1]
    assert "/" not in uuid, error_message
    assert uuid != "", error_message

    if "?" in uuid:
        uuid = uuid.split("?")[0]

    return uuid


Logger = Callable[[str], None]


# BddMessage and subclasses are used to parse websocket message formats
class BddMessage:
    def __init__(self, message: str | dict, on_error: Logger, on_success: Logger):
        self.data = message if isinstance(message, dict) else json.loads(message)
        self.on_error = on_error
        self.on_success = on_success

    def process(self):
        self.on_success(str(self.data))

    @staticmethod
    def from_message(
        message: str, on_error: Logger, on_success: Logger
    ) -> "BddMessage":
        data = json.loads(message)

        if "NotificationCreated" in data:
            return NotificationCreatedMessage(message, on_error, on_success)
        elif "LessonSubmissionEvent" in data:
            return LessonSubmissionEventMessage(message, on_error, on_success)
        else:
            return BddMessage(message, on_error, on_success)


class NotificationCreatedMessage(BddMessage):
    def process(self):
        data = self.data["NotificationCreated"]
        notification_type = data["NotificationType"]
        notification_data = data["NotificationData"]
        self.on_success(f"Nofication created: {notification_type}, {notification_data}")


class LessonSubmissionEventMessage(BddMessage):
    def process(self):
        data = self.data["LessonSubmissionEvent"]
        err = data.get("Err") or data.get("StructuredErrHTTPTest")
        if err:
            self.on_error(f"[incorrect]: {err}")
        else:
            self.on_success("Correct!")


class LessonParsingError(Exception):
    pass


def parse_lesson_api_payload(payload: Any):
    if not isinstance(payload, dict):
        raise LessonParsingError("Unrecognized api payload. Cannot parse.")
    try:
        l = payload["Lesson"]
        course_uuid = l["CourseUUID"]
        chapter_uuid = l["ChapterUUID"]
        uuid = l["UUID"]
        lesson_type = l["Type"]

        match lesson_type:
            case lesson.LessonType.CODE:
                file_content = l["LessonDataCodeCompletion"]
                starter_files = {
                    f["Name"]: f["Content"] for f in file_content["StarterFiles"]
                }

                return lesson.Lesson(
                    course_uuid=course_uuid,
                    chapter_uuid=chapter_uuid,
                    uuid=uuid,
                    lesson_type=lesson_type,
                    prog_lang=file_content["ProgLang"],
                    readme=file_content["Readme"],
                    files=starter_files,
                )

            case lesson.LessonType.CODE_TESTS:
                file_content = l["LessonDataCodeTests"]
                starter_files = {
                    f["Name"]: f["Content"] for f in file_content["StarterFiles"]
                }

                return lesson.Lesson(
                    course_uuid=course_uuid,
                    chapter_uuid=chapter_uuid,
                    uuid=uuid,
                    lesson_type=lesson_type,
                    prog_lang=file_content["ProgLang"],
                    readme=file_content["Readme"],
                    files=starter_files,
                )
            case lesson.LessonType.CLI_COMMAND:
                return lesson.Lesson(
                    course_uuid=course_uuid,
                    chapter_uuid=chapter_uuid,
                    uuid=uuid,
                    lesson_type=lesson_type,
                    prog_lang="na",
                    readme=l["LessonDataCLICommand"]["Readme"],
                    files={},
                )
            case lesson.LessonType.HTTP_TESTS:
                return lesson.Lesson(
                    course_uuid=course_uuid,
                    chapter_uuid=chapter_uuid,
                    uuid=uuid,
                    lesson_type=lesson_type,
                    prog_lang="na",
                    readme=l["LessonDataHTTPTests"]["Readme"],
                    files={},
                )
            case lesson.LessonType.CHOICE:
                question_page_payload = l["LessonDataMultipleChoice"]["Question"]
                question = question_page_payload["Question"]
                answers = "\n\n".join(question_page_payload["Answers"])
                return lesson.Lesson(
                    course_uuid=course_uuid,
                    chapter_uuid=chapter_uuid,
                    uuid=uuid,
                    lesson_type=lesson_type,
                    prog_lang="na",
                    readme=l["LessonDataMultipleChoice"]["Readme"],
                    files={"question.md": f"{question}\n{answers}"},
                )
            case lesson.LessonType.MANUAL:
                return lesson.Lesson(
                    course_uuid=course_uuid,
                    chapter_uuid=chapter_uuid,
                    uuid=uuid,
                    lesson_type=lesson_type,
                    prog_lang="na",
                    readme=l["LessonDataManual"]["Readme"],
                    files={},
                )

            case _:
                raise LessonParsingError(f"Unrecognized lesson type '{lesson_type}'")
    except KeyError as e:
        raise LessonParsingError(e)
