Contributing
=============

To contribute, start by cloning this repo:

.. code-block:: bash

  git clone https://github.com/ZaxR/bulwark.git

Create a feature branch off of the develop branch:

.. code-block:: bash

  git checkout develop
  git checkout -b feature/<snake_case_feature_name>

Docstrings and tests required for any new functions/classes/modules.
Plesae use Google-formatted docstrings.

Rebuild the docs in your local version using:

.. code-block:: bash

  sphinx-apidoc -o ./docs/_source ./bulwark
  cd docs
  make html

Create a PR to the develop branch.

Tests will be be triggered to run via `Travis CI`_.

.. _Travis CI: https://travis-ci.com/ZaxR/bulwark