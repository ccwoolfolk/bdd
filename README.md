# bdd

## Development

`source bdd-venv/bin/activate`

### Install dependencies

`python3 -m pip install -r requirements.txt`

### Add a dependency
```
python3 -m pip install [package]
python3 -m pip freeze > requirements.txt
```

## Roadmap

- bdd init
- creates env
- prompt for options
  - editor
  - open editor?
  - save options
  - notify about jwt
- bdd auth [jwt]
  - validate
  - save
- bdd get [url]
  - if exists, prompt for confirmation
  - download files
  - if auth error, notify
  - if open editor option, open
  - set most recent
- bdd run [optional uuid]
  - run the most recent if no uuid
  - notify on error
  - output to stdout
- bdd submit [optional uuid]
  - same as run, then submit
  - on success, prompt for auto advance
- bdd next [optional uuid]
- bdd prev [optional uuid]
