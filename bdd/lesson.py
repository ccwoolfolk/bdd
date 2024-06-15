from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bdd.bddio import to_bdd_path, write_data

LESSON_BASE_PATH = "lessons"


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
    def lesson_dir(self) -> Path:
        return to_bdd_path(f"{LESSON_BASE_PATH}/{self.uuid}")

    @property
    def file_paths(self) -> list[Path]:
        lesson_dir = self.lesson_dir
        return [Path(lesson_dir, nm) for nm in ("readme.md", *self.files.keys())]

    # TODO: This should probably be in a boot.dev service
    @staticmethod
    def from_api_payload(payload: Any) -> "Lesson":
        if not isinstance(payload, dict):
            raise LessonParsingError("Unrecognized api payload. Cannot parse.")
        try:
            l = payload["Lesson"]
            file_content = l["LessonDataCodeTests"]
            starter_files = {
                f["Name"]: f["Content"] for f in file_content["StarterFiles"]
            }

            return Lesson(
                course_uuid=l["CourseUUID"],
                chapter_uuid=l["ChapterUUID"],
                uuid=l["UUID"],
                lesson_type=l["Type"],
                prog_lang=file_content["ProgLang"],
                readme=file_content["Readme"],
                files=starter_files,
            )
        except KeyError as e:
            raise LessonParsingError(e)

    def save(self):
        files_to_write = {**self.files, "readme.md": self.readme}
        for file_name, file_contents in files_to_write.items():
            write_data(file_contents, str(Path(self.lesson_dir, file_name)))
        # TODO: Write metadata
