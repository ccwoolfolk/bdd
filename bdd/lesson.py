from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import bddservice
from .bddio import (
    check_exists,
    get_file_paths_from_dir,
    to_bdd_path,
    load_text,
    read_data,
    write_data,
)

LESSON_BASE_PATH = "lessons"
README_FILENAME = "readme.md"
METADATA_FILENAME = "metadata.json"


class ProgLang:
    GO = "go"
    PYTHON = "py"
    JAVASCRIPT = "js"


class LessonType:
    CHOICE = "type_choice"
    CLI_COMMAND = "type_cli_command"
    CODE = "type_code"
    CODE_TESTS = "type_code_tests"
    HTTP_TESTS = "type_http_tests"
    MANUAL = "type_manual"


SUPPORTED_LESSON_TYPES = {
    LessonType.CHOICE,
    LessonType.CLI_COMMAND,
    LessonType.CODE,
    LessonType.CODE_TESTS,
    LessonType.HTTP_TESTS,
    LessonType.MANUAL,
}


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
    def check_exists(uuid: str) -> bool:
        return check_exists(Lesson.make_lesson_dir(uuid))

    @staticmethod
    def from_disk(uuid: str) -> "Lesson":
        lesson_dir = Lesson.make_lesson_dir(uuid)
        metadata_path = str(Path(lesson_dir, METADATA_FILENAME))
        metadata = read_data(metadata_path)
        assert isinstance(metadata, dict), f"Metadata file in {uuid} is invalid"

        readme_path = str(Path(lesson_dir, README_FILENAME))
        readme = read_data(readme_path)
        assert isinstance(readme, str), f"Readme file in {uuid} is invalid"

        other_file_paths = [
            fn
            for fn in get_file_paths_from_dir(lesson_dir)
            if fn not in (metadata_path, readme_path)
        ]

        files = {}
        for p in other_file_paths:
            nm = p.split("/")[-1]
            content = load_text(p)
            files[nm] = content

        return Lesson(
            course_uuid=metadata["course_uuid"],
            chapter_uuid=metadata["chapter_uuid"],
            uuid=uuid,
            lesson_type=metadata["type"],
            prog_lang=metadata["prog_lang"],
            readme=readme,
            files=files,
        )

    @staticmethod
    def from_api_payload(payload: Any) -> "Lesson":
        return bddservice.parse_lesson_api_payload(payload)

    def save(self):
        files_to_write = {
            **self.files,
            README_FILENAME: self.readme,
            METADATA_FILENAME: self.metadata,
        }
        for file_name, file_contents in files_to_write.items():
            write_data(file_contents, str(Path(self.lesson_dir, file_name)))
