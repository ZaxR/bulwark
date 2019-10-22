#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import find_packages, setup

from bulwark import project_info

cmdclass = {}
try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print('WARNING: sphinx not available, not building docs')

with open("README.md") as readme_file:
    readme = readme_file.read()

# Requirements placed here for convenient viewing
install_requires = ['numpy>=1.8', 'pandas>=0.16.2']
tests_requires = ["pytest", "pytest-cov"]
docs_requires = ["m2r", "setuptools>=30.4", "Sphinx", "sphinx_rtd_theme"]
dev_requires = tests_requires + docs_requires + ["pre-commit", "tox"]

name = project_info.NAME
author = project_info.AUTHOR
copyright = project_info.COPYRIGHT_YEAR
version = project_info.VERSION
release = project_info.RELEASE

# Avoid setuptools as an entrypoint unless it's the only way to do it.
# In other words, only use setuptools to build dists and wheels.
# E.g.: Run tests with pytest or tox; build sphinx directly; etc.
setup(
    name=name,
    version=release,
    description='A python package for defensive data analysis.',
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/zaxr/bulwark",
    author=author,
    author_email="zaxr@protonmail.com",
    classifiers=["Development Status :: 4 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.5",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7"],
    keywords='data analysis testing',
    packages=find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.5",
    install_requires=install_requires,
    # Deprecated: setup_requires, tests_require, test_suite
    # Each extra exists for purpose k, and requires install of v.
    extras_require={'docs': docs_requires,
                    'test': tests_requires,
                    'dev': dev_requires},
    cmdclass=cmdclass,
)
