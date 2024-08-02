# bdd

## Prereqs

This tool relies on the [Boot.dev CLI](https://github.com/bootdotdev/bootdev/tree/main) to simplify initial authentication. Install the tool and run `bootdev login` before attempting to use `bdd`.

Python `3.10` or greater is recommended.

## Usage

Run `bdd init` to set up your configuration.

`bdd connect` will open a websocket connection to receive success/failure messages when submitting lessons. You will likely want this in a visible terminal while working.

`bdd get [Boot.dev lesson URL]` will retrieve the lesson files and open them with the editor stored in your configuration.

`bdd next` and `bdd prev` will move between lessons. `bdd get` without a URL will get the lesson contents based on your current position. This is useful after changing position and also for resuming work after exiting your editor.

`bdd run` and `bdd submit` function similarly to the respective Boot.dev commands.

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

Given that we are reverse engineering, it's important to understand how boot.dev lessons actually work. At a high level:

* Each lesson has a "type". Some are multiple choice questions, some rely on submitting commands from the command line, etc.
* There is a partially unique payload for each type. E.g., a multiple choice lesson payload includes the question and possible answers in its payload while a code test lesson payload includes source code and tests.
* Lessons are returned in JSON format with a top-level `Lesson` key. `Lesson` contains many fields shared amongst lesson types (`UUID`, `Type`, etc.) as well as type-specific `LessonData[type]` fields that are null for all types except the lesson's type. For example, a `type_code` lesson will have a `LessonDataCodeCompletion` key with a non-null value.
* Most lessons consist of 3 operations: 1) Retrieving the lesson data. 2) `run`ning the lesson which typically executes the student's code or runs against a subset of automated tests. 3) `submit`ting which sends the full result (all automated tests if applicable) to boot.dev for evaluation. Multiple choice questions don't have a `run` operation; code lessons without tests obviously don't have different tests to `run` vs `submit`; etc. Basically, the distinction between `run` and `submit` varies based on lesson type.

### In the browser

When you load a lesson on boot.dev, a `GET` request is made to the api for that lesson's payload. The lesson's `Readme.md` is typically displayed on the left with a code environment or mulitple choice block on the right, depending on the lesson type.

A websocket connection is initiated if one doesn't already exists. This connection facilitates the success/failure message you see as popups. Somewhat surprisingly, these don't seem to be direct results of the submit response in the browser. This is likely to support command line lessons which are not submitted from the browser but can still behave similarly.

Several more requests are made on page load. These facilitate gamification elements, conversations with Boots, user analytics for the boot.dev team, etc. If gamification is important to you, you will have a better experience in the browser as `bdd` does not attempt to replicate or display these.

You might expect boot.dev to execute your Go or Python code in a server environment, but boot.dev code lessons run code in the browser. One implication of this approach is that "submitting" a lesson generally means submitting the result of your code rather than the code itself. (This is a totally reasonable choice for boot.dev, but it's a bit inconvenient for `bdd` because it means the package has to handle executing code instead of simply submitting source code.)

You also might expect your code to be stored by boot.dev, but your code is saved only to local storage (another great complexity tradeoff decision, IMO). This is convenient for `bdd` because the package doesn't have to worry about syncing your input state -- any code you write in the browser stays in the browser, and `bdd get` will give you a fresh set of files.

### Data Keys by Lesson Type

| type_choice       | `LessonDataMultipleChoice` |
| type_cli_command       | `LessonDataCLICommand` |
| type_code       | `LessonDataCodeCompletion` |
| type_code_tests | `LessonDataCodeTests` |
| type_http_tests | `LessonDataHTTPTests` |

### Example Lesson URLs

| type_choice       | n/a     | TODO |
| type_cli_command       | n/a     | TODO |
| type_code       | go     | https://www.boot.dev/lessons/224252be-adc9-452f-8ed0-0b305b25d0cb |
| type_code       | python |                                                                   |
| type_code_tests | go     | https://www.boot.dev/lessons/d8b6aaab-5a7c-4fb9-b8d8-82297029057a |
| type_code_tests | python | https://www.boot.dev/lessons/acb5117d-0f34-40b3-81f0-b89828f0e443 |
| type_http_tests | TODO | TODO |

## Roadmap

### type_code

Example submit:

```
POST https://api.boot.dev/v1/lessons/224252be-adc9-452f-8ed0-0b305b25d0cb/code
{output: "starting Textio server..."}
res: 200 {}
```

### type_code_tests

If python:
```javascript
fullCode = e.data.withSubmit
              ? "__SUBMIT__ = True;" + fullCode
              : "__RUN__ = True;" + fullCode;
```
where `fullCode` is `main_test.py`. Note that the check isn't for truth equality, it is merely for the key's presence in `globals()`. I.e., don't add both and set one to false.

If go:
```javascript
if (e.data.withSubmit) {
      self.withSubmit = true;
}
```

and:
```go
//·withSubmit·is·set·at·compile·time·depending
//·on·which·button·is·used·to·run·the·tests
var·withSubmit·=·true
```
in `main_test.go`.

### run

Note that withSubmit needs to be set to false.

### submit

The only string that seems to matter for Go code is:
```json
  {"output": "- FAIL:"}
```

Any change to this string results in a pass.

Note the output looks compressed in the api call below. This is compared to a local output of:

```
=== RUN   Test
Test Passed: (10) => expected: 10.45, actual: 10.45
Test Passed: (20) => expected: 21.90, actual: 21.90
Test Passed: (0) => expected: 0.00, actual: 0.00
Test Passed: (1) => expected: 1.00, actual: 1.00
Test Passed: (5) => expected: 5.10, actual: 5.10
Test Passed: (30) => expected: 34.35, actual: 34.35
--- PASS: Test (0.00s)
PASS
ok      command-line-arguments  0.002s
```

Example submit:

```
POST https://api.boot.dev/v1/lessons/d8b6aaab-5a7c-4fb9-b8d8-82297029057a/code_tests
{
    "output": "Test Passed: (10) => expected: 10.45, actual: 10.45Test Passed: (20) => expected: 21.90, actual: 21.90Test Passed: (0) => expected: 0.00, actual: 0.00Test Passed: (1) => expected: 1.00, actual: 1.00Test Passed: (5) => expected: 5.10, actual: 5.10Test Passed: (30) => expected: 34.35, actual: 34.35PASS"
}
```
