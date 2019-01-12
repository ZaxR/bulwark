#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages
# from sphinx.setup_command import BuildDoc

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    print('WARNING: sphinx not available, not building docs')


with open("README.md") as readme_file:
    readme = readme_file.read()

# Requirements placed here for convenient viewing
setup_requires = ["pytest-runner"]
install_requires = ['numpy', 'pandas', 'six']
tests_requires = ["coverage", "pytest"]
dev_requires = ["Sphinx", "sphinx_rtd_theme"]

# cmdclass = {'build_sphinx': BuildDoc}


name = "bulwark"
copyright = "2019"
version = '0.1'
release = '0.1.1'
setup(
    name=name,
    version=release,
    description='A python package for defensive data analysis.',
    long_description=readme,
    url="https://github.com/zaxr/bulwark",
    author="Zax Rosenberg",
    author_email="zaxr@protonmail.com",
    classifiers=["Development Status :: 3 - Alpha",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Natural Language :: English",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7"],
    keywords='data analysis, testing',
    packages=find_packages(exclude=["docs", "tests"]),
    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_requires,
    test_suite="tests",
    extras_require={'dev': dev_requires},
    cmdclass=cmdclass,
    # these are optional and override conf.py settings
    command_options={'build_sphinx': {"project": ("setup.py", name),
                                      "copyright": ("setup.py", copyright),
                                      "version": ("setup.py", version),
                                      "release": ("setup.py", release),
                                      "source_dir": ("setup.py", "docs")}}
)
