# battenberg-gitlab

[![image](https://img.shields.io/pypi/v/battenberg-gitlab.svg)](https://pypi.python.org/pypi/battenberg-gitlab)
[![image](https://img.shields.io/travis/zillow/battenberg-gitlab.svg)](https://travis-ci.org/zillow/battenberg-gitlab)

Automatically running [battenberg](https://github.com/zillow/battenberg) on a series of Gitlab repos.

## Installation

TODO

## Usage

TODO

## Development

To get set up run:

```bash
python3 -m venv env
source env/bin/activate

# Install in editable mode so you get the updates propagated.
pip install -e .

# If you want to be able to run tests & linting install via:
pip install -e ".[dev]"
```

Then to actually perform any operations just use the `battenberg_gitlab` command which should now be on your `$PATH`.

To run tests:

```bash
pytest
```

To run linting:

```bash
flake8 --config flake8.cfg battenberg_gitlab
```

## License

Free software: Apache Software License 2.0
