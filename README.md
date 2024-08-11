# bdd

`bdd` is a command line tool for completing [Boot.dev](https://boot.dev) lessons in the terminal.

**Why?** The Boot.dev web interface is great. If you find the videos helpful or enjoy the gamification elements, stick to the web interface. But if you want to hone your skills in the command line and gain familiarity with your editor, give `bdd` a try.

Interested in contributing? Check out the [contribution guidelines](docs/CONTRIBUTING.md).

## Prereqs

This tool relies on the [Boot.dev CLI](https://github.com/bootdotdev/bootdev/tree/main) to simplify initial authentication. Install the tool and run `bootdev login` before attempting to use `bdd`.

Python `3.10` or greater is recommended.

Windows file paths are not supported at this time but [could be](docs/CONTRIBUTING.md).

## Usage

Run `bdd init` to set up your configuration. You will specify how to run go python (ex: `python` vs `python3`), go (ex: `go` vs `go[version]`), etc. Note that the editor command should accept a list of files to open. For example, `nvim -p` (default) for Neovim, `code` for VS Code, or a `/mnt/c/Program Files/` path if you code in the [best IDE for programming](https://youtu.be/X34ZmkeZDos).

`bdd connect` will open a websocket connection to receive success/failure messages when submitting lessons. You will likely want this in a visible terminal while working.

`bdd get [Boot.dev lesson URL]` will retrieve the lesson files and open them with the editor stored in your configuration.

`bdd next` and `bdd prev` will move between lessons. `bdd get` without a URL will get the lesson contents based on your current position. This is useful after changing position and also for resuming work after exiting your editor.

`bdd run` and `bdd submit` function similarly to the respective Boot.dev commands.

`bdd progress` will show your progress in the current course, including lesson completion status.

## Development

### Virtual environment

Create your virtual environment. I recommend `venv` which is part of the standard library as of `3.3`.

```bash
python3 -m venv .venv
```

and activate it with `source .venv/bin/activate`.

### Install for development with dependencies

`python3 -m pip install -e .[dev]`

### Add a dependency

Add to `pyproject.yaml` then repeat the `pip install` command above.

### Manual testing

```bash
bdd --help
```

### Automated testing

After following the dev installation steps:

```bash
pytest
```

## How boot.dev lessons work

`bdd` essentially relies on an undocumented, internal set of boot.dev APIs and conventions. Yes, this is gross, and it will definitely break as changes are made to the platform. The "bet" is that the functionality will be worth this inconvenience.

See [bdd.md](docs/bdd.md) for more information on how boot.dev lessons work and some examples.
