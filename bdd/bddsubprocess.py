import subprocess
from .bddconfig import BddConfig


def run_go(file_path: str) -> subprocess.CompletedProcess[str]:
    cmd = BddConfig().go_command.value
    return subprocess.run([cmd, "run", file_path], capture_output=True, text=True)


def run_go_test(
    lesson_dir: str, file_names: list[str]
) -> subprocess.CompletedProcess[str]:
    cmd = BddConfig().go_command.value
    test_args = [cmd, "test", "-v", *file_names]
    return subprocess.run(test_args, capture_output=True, text=True, cwd=lesson_dir)


def run_python(
    file_path: str, cwd: str, is_submit: bool
) -> subprocess.CompletedProcess[str]:
    # Wrap the test file in a temporary script where we can set run vs submit. We
    # could instead prepend the variable assignment to the test file, but this
    # approach avoids creating any differences in the local file and the boot.dev
    # version. It's also annoying to have a file change while it is likely open in
    # the student's editor.
    cmd = BddConfig().python_command.value
    py_var = "__SUBMIT__" if is_submit else "__RUN__"
    py_command = "\n".join(
        [
            f"{py_var} = True",
            f"with open('{file_path}') as f:",
            "\tcontents = f.read()",
            "\texec(contents)",
        ]
    )
    return subprocess.run(
        [cmd, "-c", py_command],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def run_js(file_path: str) -> subprocess.CompletedProcess[str]:
    cmd = BddConfig().js_command.value
    return subprocess.run([cmd, file_path], capture_output=True, text=True)
