import subprocess


def run_go(file_path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["go", "run", file_path], capture_output=True, text=True)


def run_go_test(
    lesson_dir: str, file_names: list[str]
) -> subprocess.CompletedProcess[str]:
    test_args = ["go", "test", "-v", *file_names]
    return subprocess.run(test_args, capture_output=True, text=True, cwd=lesson_dir)


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


def run_js(file_path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["node", file_path], capture_output=True, text=True)
