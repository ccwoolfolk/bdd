from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .bddio import to_bdd_path, read_data, write_data

LESSON_BASE_PATH = "lessons"
README_FILENAME = "readme.md"
METADATA_FILENAME = "metadata.json"


class ProgLang:
    GO = "go"
    PYTHON = "py"


class LessonType:
    CHOICE = "type_choice"
    CLI_COMMAND = "type_cli_command"
    CODE = "type_code"
    CODE_TESTS = "type_code_tests"
    HTTP_TESTS = "type_http_tests"


SUPPORTED_LESSON_TYPES = {
    LessonType.CHOICE,
    LessonType.CLI_COMMAND,
    LessonType.CODE,
    LessonType.CODE_TESTS,
    LessonType.HTTP_TESTS,
}


class LessonParsingError(Exception):
    pass


@dataclass
class Lesson:
    course_uuid: str
    chapter_uuid: str
    uuid: str
    lesson_type: str
    prog_lang: str
    readme: str
    files: dict[str, str]

    @property
    def is_supported_lesson_type(self) -> bool:
        return self.lesson_type in SUPPORTED_LESSON_TYPES

    @property
    def lesson_dir(self) -> Path:
        return Lesson.make_lesson_dir(self.uuid)

    @property
    def file_paths(self) -> list[Path]:
        lesson_dir = self.lesson_dir
        return [Path(lesson_dir, nm) for nm in (README_FILENAME, *self.files.keys())]

    @property
    def metadata(self) -> dict[str, Any]:
        return {
            "type": self.lesson_type,
            "prog_lang": self.prog_lang,
            "course_uuid": self.course_uuid,
            "chapter_uuid": self.chapter_uuid,
            "uuid": self.uuid,
        }

    @staticmethod
    def make_lesson_dir(uuid: str) -> Path:
        return to_bdd_path(f"{LESSON_BASE_PATH}/{uuid}")

    @staticmethod
    def from_disk(uuid: str) -> "Lesson":
        lesson_dir = Lesson.make_lesson_dir(uuid)
        metadata = read_data(str(Path(lesson_dir, METADATA_FILENAME)))
        assert isinstance(metadata, dict), f"Metadata file in {uuid} is invalid"
        readme = read_data(str(Path(lesson_dir, README_FILENAME)))
        assert isinstance(readme, str), f"Readme file in {uuid} is invalid"

        # TODO: finish adding files here
        return Lesson(
            course_uuid=metadata["course_uuid"],
            chapter_uuid=metadata["chapter_uuid"],
            uuid=uuid,
            lesson_type=metadata["type"],
            prog_lang=metadata["prog_lang"],
            readme=readme,
            files={},
        )

    # TODO: This should probably be in a boot.dev service
    @staticmethod
    def from_api_payload(payload: Any) -> "Lesson":
        if not isinstance(payload, dict):
            raise LessonParsingError("Unrecognized api payload. Cannot parse.")
        try:
            l = payload["Lesson"]
            course_uuid = l["CourseUUID"]
            chapter_uuid = l["ChapterUUID"]
            uuid = l["UUID"]
            lesson_type = l["Type"]

            match lesson_type:
                case LessonType.CODE:
                    file_content = l["LessonDataCodeCompletion"]
                    starter_files = {
                        f["Name"]: f["Content"] for f in file_content["StarterFiles"]
                    }

                    return Lesson(
                        course_uuid=course_uuid,
                        chapter_uuid=chapter_uuid,
                        uuid=uuid,
                        lesson_type=lesson_type,
                        prog_lang=file_content["ProgLang"],
                        readme=file_content["Readme"],
                        files=starter_files,
                    )

                case LessonType.CODE_TESTS:
                    file_content = l["LessonDataCodeTests"]
                    starter_files = {
                        f["Name"]: f["Content"] for f in file_content["StarterFiles"]
                    }

                    return Lesson(
                        course_uuid=course_uuid,
                        chapter_uuid=chapter_uuid,
                        uuid=uuid,
                        lesson_type=lesson_type,
                        prog_lang=file_content["ProgLang"],
                        readme=file_content["Readme"],
                        files=starter_files,
                    )
                case LessonType.CLI_COMMAND:
                    return Lesson(
                        course_uuid=course_uuid,
                        chapter_uuid=chapter_uuid,
                        uuid=uuid,
                        lesson_type=lesson_type,
                        prog_lang="na",
                        readme=l["LessonDataCLICommand"]["Readme"],
                        files={},
                    )
                case LessonType.HTTP_TESTS:
                    return Lesson(
                        course_uuid=course_uuid,
                        chapter_uuid=chapter_uuid,
                        uuid=uuid,
                        lesson_type=lesson_type,
                        prog_lang="na",
                        readme=l["LessonDataHTTPTests"]["Readme"],
                        files={},
                    )
                case LessonType.CHOICE:
                    question_page_payload = l["LessonDataMultipleChoice"]["Question"]
                    question = question_page_payload["Question"]
                    answers = "\n\n".join(question_page_payload["Answers"])
                    return Lesson(
                        course_uuid=course_uuid,
                        chapter_uuid=chapter_uuid,
                        uuid=uuid,
                        lesson_type=lesson_type,
                        prog_lang="na",
                        readme=l["LessonDataMultipleChoice"]["Readme"],
                        files={"question.md": f"{question}\n{answers}"},
                    )

                case _:
                    # TODO: don't raise on other lesson types
                    raise LessonParsingError(
                        f"Unrecognized lesson type '{lesson_type}'"
                    )
        except KeyError as e:
            raise LessonParsingError(e)

    def save(self):
        files_to_write = {
            **self.files,
            README_FILENAME: self.readme,
            METADATA_FILENAME: self.metadata,
        }
        for file_name, file_contents in files_to_write.items():
            write_data(file_contents, str(Path(self.lesson_dir, file_name)))
