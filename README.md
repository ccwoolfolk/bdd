# bdd

## Prereqs

This tool relies on the [Boot.dev CLI](https://github.com/bootdotdev/bootdev/tree/main) to simplify initial authentication. Install the tool and run `bootdev login` before attempting to use `bdd`.

Python `3.10` or greater is recommended.

## Usage

Run `bdd init` to set up your configuration.

`bdd get [Boot.dev lesson URL]` will retrieve the lesson files and open them with the editor stored in your configuration.

## Development

### Virtual environment

Create your virtual environment. I recommend `venv` which is part of the standard library as of `3.3`.

```bash
python3 -m venv .venv
```

and activate it with `source .venv/bin/activate`.

### Install dependencies

`python3 -m pip install -r requirements.txt`

### Add a dependency

```bash
python3 -m pip install [package]
python3 -m pip freeze > requirements.txt
```

### Manual testing

```bash
python3 -m pip install --editable .
bdd --help
```

## Roadmap

- bdd init
  - prompt for options
    - open editor?
- bdd run [optional uuid]
  - run the most recent if no uuid
  - notify on error
  - output to stdout
- bdd submit [optional uuid]
  - same as run, then submit
  - on success, prompt for auto advance
- bdd next [optional uuid]
- bdd prev [optional uuid]
