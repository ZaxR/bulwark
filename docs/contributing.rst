Contributing
=============

Set up Git and a GitHub Account
-------------------------------
- If you don't already have a GitHub account, you can register for free.
- If you don't already have Git installed, you can follow these `git installation instructions`_.

.. _git installation instructions: https://help.github.com/en/articles/set-up-git

Fork and Clone Bulwark
----------------------
1. You will need your own fork to work on the code. Go to the `Bulwark project page`_ and hit the Fork button. 
2. Next, you'll want to clone your fork to your machine:

.. code-block:: bash

  git clone https://github.com/your-user-name/bulwark.git bulwark-dev
  cd bulwark-dev
  git remote add upstream https://github.com/ZaxR/bulwark.git


.. _Bulwark project page: https://github.com/ZaxR/bulwark


Set up a Development Environment
--------------------------------
Bulwark supports Python 3.5+. It's recommended to use version 3.5 for development to ensure newer features aren't accidentally used, though CI tools will check all versions on the creation of a PR.


Create a Feature Branch
--------------------------------
Bulwark loosely follows the gitflow workflow. To add a new feature, you will create every feature branch off of the develop branch:

.. code-block:: bash

  git checkout develop
  git checkout -b feature/<feature_name_in_snake_case>


Development Practices and Standards
-----------------------------------
- Unit tests covering added/changed code are required for a PR to be merged. There is currently no CI check for coverage, but this will be manually enforced. Test-Driven Development (TDD) is encouraged.
- Any new module, class, or function requires a docstring, in the `Google docstring format`_.
- Please follow PEP-8 

.. _Google docstring format: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html


Create a Pull Request to the develop branch
-------------------------------------------
`Create a pull request`_ to the develop branch of Bulwark. Tests will be be triggered to run via `Travis CI`_. Check that your PR doesn't fail any tests, since it won't be reviewed for inclusion until it passes all tests.

.. _Create a pull request: https://help.github.com/en/articles/creating-a-pull-request-from-a-fork
.. _Travis CI: https://travis-ci.com/ZaxR/bulwark


For Maintainers
---------------
When it's time to create a release candidate, a new branch should be created from develop:

.. code-block:: bash

  git checkout develop
  git checkout -b release/x.x.x

However, several additional steps must also be taken: 

1. Update version in project_info.py, which updates three spots: setup.py, bulwark/__init__.py, and docs/conf.py
2. Update the CHANGELOG.md/changelog.rst and the main README.md/index.rst (as appropriate).
3. Rebuild the docs in your local version using:

.. code-block:: bash

  pip install -e ".[dev]"
  sphinx-apidoc -o ./docs/_source ./bulwark -f
  cd docs
  make html

4. Test distribution using TestPyPI with Twine 

.. code-block:: bash

  # Installation
  python3 -m pip install --user --upgrade setuptools wheel
  python3 -m pip install --user --upgrade twine

  # Build/Upload dist and install library
  python3 setup.py sdist bdist_wheel
  python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
  pip install --index-url https://test.pypi.org/simple/ bulwark

4. Merge the release candidate into both master (which will trigger updates for PyPi and readthedocs) and develop.