Contributing
=============

To contribute, start by cloning this repo:

.. code:: bash
   git clone https://github.com/ZaxR/bulwark.git

Create a feature branch off of the develop branch:

.. code:: bash
   git checkout develop
   git checkout -b feature/<snake_case_feature_name>

Rebuild the docs in your local version using 

.. code:: bash
   sphinx-apidoc -o ./docs/_source ./bulwark
   cd docs
   make html

Create a PR to the develop branch.