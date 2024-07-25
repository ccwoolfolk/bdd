import datetime
import json
from typing import Callable
import os
from pathlib import Path
import subprocess

from . import client
from . import progress
from .lesson import Lesson, LessonParsingError, LessonType, ProgLang
from .bddconfig import BddConfig


# TODO: move code execution fns
def run_go(file_path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["go", "run", file_path], capture_output=True, text=True)


def run_go_test(lesson_dir: str, file_names: list[str]):
    test_args = ["go", "test", "-v", *file_names]
    return subprocess.run(test_args, capture_output=True, text=True, cwd=lesson_dir)


def _replace_in_file(file_path: Path | str, from_text: str, to_text: str):
    # Use this for go tests because the variable assignment for withSubmit is
    # embedded directly into the source code. It's gross to mutate the file, but I
    # can't see a workaround like creating a temp file being a good complexity vs
    # value tradeoff.
    with open(file_path, "r") as f:
        text = f.read()
    new_text = text.replace(from_text, to_text)
    with open(file_path, "w") as f:
        f.write(new_text)


def run_python(file_path: str, is_submit: bool) -> subprocess.CompletedProcess[str]:
    # TODO: make python/python3 configurable
    # Wrap the test file in a temporary script where we can set run vs submit. We
    # could instead prepend the variable assignment to the test file, but this
    # approach avoids creating any differences in the local file and the boot.dev
    # version. It's also annoying to have a file change while it is likely open in
    # the student's editor.
    py_var = "__SUBMIT__" if is_submit else "__RUN__"
    py_command = "\n".join(
        [f"{py_var} = True", f"with open('{file_path}') as f:", "\texec(f.read())"]
    )
    return subprocess.run(["python3", "-c", py_command], capture_output=True, text=True)


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


def run_lesson(is_submit: bool = False) -> str | None:
    uuid = progress.get_current_lesson_uuid()
    lesson = Lesson.from_disk(uuid)

    match lesson.lesson_type:
        case LessonType.CODE | LessonType.CODE_TESTS:
            is_test = lesson.lesson_type == LessonType.CODE_TESTS

            match lesson.prog_lang:
                # TODO: don't hardcode main.go, main.py, etc.
                case ProgLang.GO:
                    if is_test:
                        test_path = Path(lesson.lesson_dir, "main_test.go")
                        if is_submit:
                            _replace_in_file(
                                test_path,
                                from_text="withSubmit = false",
                                to_text="withSubmit = true",
                            )
                        else:
                            _replace_in_file(
                                test_path,
                                from_text="withSubmit = true",
                                to_text="withSubmit = false",
                            )
                        results = run_go_test(
                            str(lesson.lesson_dir), ["main_test.go", "main.go"]
                        )
                    else:
                        results = run_go(str(Path(lesson.lesson_dir, "main.go")))
                case ProgLang.PYTHON:
                    fn: str = "main_test.py" if is_test else "main.py"
                    results = run_python(
                        str(Path(lesson.lesson_dir, fn)), is_submit=is_submit
                    )
                case _:
                    raise NotImplementedError()

            try:
                results.check_returncode()
            except subprocess.CalledProcessError:
                output = "\n".join([results.stdout, results.stderr])
                raise CommandError(output)
            return results.stdout

        case LessonType.CLI_COMMAND | LessonType.HTTP_TESTS:
            # We are Very Smart so we pass the work to the bootdev cli
            os.system(f"bootdev run {uuid}")
        case LessonType.CHOICE | LessonType.MANUAL:
            raise CommandError("This lesson type doesn't support `run`.")
        case _:
            raise NotImplementedError()


def submit_lesson(submission: str | None):
    uuid = progress.get_current_lesson_uuid()
    lesson = Lesson.from_disk(uuid)

    match lesson.lesson_type:
        case LessonType.CODE:
            results = run_lesson()
            if results is None:
                raise CommandError(
                    "Running the code produced no results. This is probably an error."
                )
            client.submit_code(results, lesson.uuid)
        case LessonType.CODE_TESTS:
            # TODO: should this set withSubmit differently?
            results = run_lesson()
            if results is None:
                raise CommandError(
                    "Running the code produced no results. This is probably an error."
                )
            client.submit_code_tests(results, lesson.uuid)
        case LessonType.CLI_COMMAND | LessonType.HTTP_TESTS:
            # We are Very Smart so we pass the work to the bootdev cli
            os.system(f"bootdev submit {uuid}")
        case LessonType.CHOICE:
            if submission is None or submission == "":
                raise CommandError(
                    'This is a multiple choice lesson. Submit like: `bdd submit "My answer here"`'
                )
            client.submit_multiple_choice(submission, uuid)
        case LessonType.MANUAL:
            client.submit_manual(uuid)
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


# TODO: move this to a boot.dev service
def get_error_from_wss_message(message: str) -> str | None:
    lesson_submission_event = json.loads(message)["LessonSubmissionEvent"]
    return (
        lesson_submission_event["Err"]
        or lesson_submission_event["StructuredErrHTTPTest"]
    )


Logger = Callable[[str], None]


def open_bdd_connection(
    *, info_logger: Logger, success_logger: Logger, error_logger: Logger
) -> None:
    def on_message(message: str):
        stamp = datetime.datetime.now().strftime("%H:%M:%S")

        error_message = get_error_from_wss_message(message)

        if error_message:
            error_logger(f"\n{stamp}: [incorrect] {error_message}")
        else:
            success_logger(f"\n{stamp}: Correct!")

    def on_error(error: str):
        # This isn't ideal, but websocket-client errors on keyboard interrupt
        # which prints an empty error when you close the connection.
        # See https://github.com/websocket-client/websocket-client/issues/964
        if error:
            error_logger(f"Error: {error}")

    def on_close():
        info_logger("Disconnected.")

    def on_open():
        info_logger("Connected.")

    client.open_bdd_ws_connection(
        on_message=on_message, on_error=on_error, on_open=on_open, on_close=on_close
    )
