# How to Contribute

First off, thank you for considering contributing to `bulwark`!
It’s thanks to people like you that we continue to have a high-quality, updated and documented tool.

There are a few key ways to contribute:

1. Writing new code (checks, decorators, other functionality)
2. Writing tests
3. Writing documentation
4. Supporting fellow developers on StackOverflow.com.

No contribution is too small!
Please submit as many fixes for typos and grammar bloopers as you can!

Regardless of which of these options you choose,
this document is meant to make contribution more accessible by codifying tribal knowledge and expectations.
Don’t be afraid to ask questions if something is unclear!

## Workflow

1. Set up Git and a GitHub account
2. Bulwark follows a [forking workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow), so next fork and clone the bulwark repo.
3. Set up a development environment.
4. Create a feature branch.
   Pull requests should be limited to one change only, where possible.
   Contributing through short-lived feature branches ensures contributions can get merged quickly and easily.
5. Rebase on master and squash any unnecessary commits.
   We do not squash on merge, because we trust our contributors to decide which commits within a feature are worth breaking out.
6. Always add tests and docs for your code.
   This is a hard rule; contributions with missing tests or documentation can’t be merged.
7. Make sure your changes pass our CI.
   You won’t get any feedback until it’s green unless you ask for it.
8. Once you’ve addressed review feedback, make sure to bump the pull request with a short note, so we know you’re done.

Each of these abbreviated workflow steps has additional instructions in sections below.


## Development Practices and Standards

- Obey follow PEP-8 and [Google's docstring format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).
  - The only exception to PEP-8 is that line length can be up to 100 characters.
- Use underscores to separate words in non-class names.
  E.g. `n_samples` rather than `nsamples`.
- Don't ever use wildcard imports (`from module import *`).
  It's considered to be a bad practice by the [official Python recommendations](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package).
  The reasons it's undesirable are that it
  pollutes the namespace,
  makes it harder to identify the origin of code,
  and, most importantly, prevents using a static analysis tool like pyflakes to automatically find bugs.
- Any new module, class, or function requires units tests and a docstring.
  Test-Driven Development (TDD) is encouraged.
- Don’t break backward compatibility.
  In the event that an interface needs redesign to add capability,
  a deprecation warning should be raised in future minor versions,
  and the change will only be merged into the next major version release.
- [Semantic line breaks](https://sembr.org/) are encouraged.


## Set up Git and a GitHub Account

- If you don't already have a GitHub account, you can register for free.
- If you don't already have Git installed,
  you can follow these [git installation instructions](https://help.github.com/en/articles/set-up-git).


## Fork and Clone Bulwark

1. You will need your own fork to work on the code. Go to the [Bulwark
   project page](https://github.com/ZaxR/bulwark) and hit the Fork
    button.
2. Next, you'll want to clone your fork to your machine:

    ```bash
    git clone https://github.com/your-user-name/bulwark.git bulwark-dev
    cd bulwark-dev
    git remote add upstream https://github.com/ZaxR/bulwark.git
    ```

## Set up a Development Environment

Bulwark supports Python 3.5+.
For your local development version of Python it's recommended to use version 3.5
within a virtual environment to ensure newer features aren't accidentally used.

Within your virtual environment,
you can easily install an editable version of `bulwark`
along with its tests and docs requirements with:

```bash
pip install -e '.[dev]'
```

At this point you should be able to run/pass tests and build the docs:

```bash
python -m pytest

cd docs
make html
```

To avoid committing code that violates our style guide,
we strongly advise you to install [pre-commit](https://pre-commit.com/) hooks,
which will cause your local commit to fail if our style guide was violated:

```bash
pre-commit install
```

You can also run them anytime (as our tox does) using:

```bash
pre-commit run --all-files
```

You can also use tox to run CI in all of the appropriate environments locally, as our cloud CI will:

```bash
tox
# or, use the -e flag for a specific environment. For example:
tox -e py35
```

## Create a Feature Branch

To add a new feature, you will create every feature branch off of the master branch:

```bash
git checkout master
git checkout -b feature/<feature_name_in_snake_case>
```

## Rebase on Master and Squash

If you are new to rebase, there are many useful tutorials online,
such as [Atlassian's](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase).
Feel free to follow your own workflow,
though if you have an default git editor set up,
interactive rebasing is an easy way to go about it:

```bash
git checkout feature/<feature_name_in_snake_case>
git rebase -i master
```

## Create a Pull Request to the master branch

[Create a pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork)
to the master branch of Bulwark.
Tests will be be triggered to run via [Travis CI](https://travis-ci.com/ZaxR/bulwark).
Check that your PR passes CI,
since it won't be reviewed for inclusion until it passes all steps.

## For Maintainers

Steps for maintainers are largely the same,
with a few additional steps before releasing a new version:

- Update version in bulwark/project\_info.py,
  which updates three spots: setup.py, bulwark/\_\_init\_\_.py, and docs/conf.py.
- Update the CHANGELOG.md and the main README.md (as appropriate).
- Rebuild the docs in your local version to verify how they render using:

    ```bash
    pip install -e ".[dev]"
    sphinx-apidoc -o ./docs/_source ./bulwark -f
    cd docs
    make html
    ```

- Test distribution using TestPyPI with Twine:

    ```bash
    # Installation
    python3 -m pip install --user --upgrade setuptools wheel
    python3 -m pip install --user --upgrade twine

    # Build/Upload dist and install library
    python3 setup.py sdist bdist_wheel
    python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    pip install bulwark --index-url https://test.pypi.org/simple/bulwark
    ```

- Releases are indicated using git tags.
  Create a tag locally for the appropriate commit in master, and push that tag to GitHub.
  Travis's CD is triggered on tags within master:

    ```bash
    git tag -a v<#.#.#> <SHA-goes-here> -m "bulwark version <#.#.#>"
    git push origin --tags
    ```
