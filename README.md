# battenberg-gitlab

[![image](https://img.shields.io/pypi/v/battenberg-gitlab.svg)](https://pypi.python.org/pypi/battenberg-gitlab)
[![image](https://img.shields.io/travis/zillow/battenberg-gitlab.svg)](https://travis-ci.org/zillow/battenberg-gitlab)

Automatically running [battenberg](https://github.com/zillow/battenberg) on a series of Gitlab repos.

## Installation

**TODO ZOMLINFRA-480 Move to install battenberg-gitlab via battenberg[gitlab] extra**

Currently we do not plan on publishing this to PyPI standalone, instead publishing it as a module underneath `battenberg`.
Until that work is done though you can install it via:

```bash
git clone git@github.com:zillow/battenberg-gitlab.git
cd battenberg-gitlab
# If you don't want to install this globally run
python3 -m venv env && source env/bin/activate
pip install .
cp python-gitlab.cfg.example python-gitlab.cfg
# Generate a Gitlab API token and paste it in as appropriate.
vi python-gitlab.cfg
```

If you're on Mac OS X or Windows please follow the [installation guides](https://www.pygit2.org/install.html#) in the `pygit2` documentation
as well as `battenberg` relies on `libgit2` which needs to be installed first.

## Usage

**TODO ZOMLINFRA-480 Move to install battenberg-gitlab via battenberg[gitlab] extra**

Once installed the general idea of `battenberg-gitlab` is to make it easy to find and clone locally a matching filterset
of Gitlab projects. To do this you can:

### Search

`battenberg_gitlab search` queries Gitlab for a set of groups and projects. It will then clone them locally and inspect
the `template` branch to determine which version they're on.

**TODO ZOMLINFRA-426 Set custom commit messages for battenberg install & upgrade commands.**

```bash
battenberg_gitlab search \
    [--project-filter <filter type>=<keyword>] \
    [--group-name <group name>] \
    [--workspace <path>]
# For example: battenberg_gitlab search --project-filter tag=archetype.py-ml --group-name zoml
```

This will return a list of all matched projects and the latest commit message from the `template` branch.

* `--project-filter` - Can be passed multiple times to narrow the search. Should follow the format `<filter type>=<keyword>`
currently the only supported `<filter type>` is `tag`.
* `--group-name` - Can be passed multiple times to expand the search.
* `--workspace` - Can be passed to override where projects are cloned to, by default `battenberg-gitlab` will create
a new directory under `/tmp`.

### Apply

```bash
battenberg_gitlab apply \
    [--checkout <version>] \
    [--project-filter <filter type>=<keyword>] \
    [--group-name <group name>] \
    [--workspace <path>]
# For example: battenberg_gitlab apply --checkout v1.1.0 --project-filter tag=archetype.py-ml --group-name zoml
```

* `--checkout` - Template branch, tag or commit to checkout to apply the upgrade from.
* `--project-filter` - See docs above for `search` command.
* `--group-name` - See docs above for `search` command.
* `--workspace` - See docs above for `search` command.

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
