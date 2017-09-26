#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import setuptools

def main():

    setuptools.setup(
        name             = "megaparsex",
        version          = "2017.09.26.1724",
        description      = "parsing and associated utilities",
        long_description = long_description(),
        url              = "https://github.com/wdbm/megaparsex",
        author           = "Will Breaden Madden",
        author_email     = "wbm@protonmail.ch",
        license          = "GPLv3",
        py_modules       = [
                           "AWRS",
                           "megaparsex"
                           ],
        install_requires = [
                           "docopt",
                           ],
        scripts          = [
                           "megaparsex.py"
                           ],
        entry_points     = """
                           [console_scripts]
                           megaparsex = megaparsex:megaparsex
                           """
    )

def long_description(
    filename = "README.md"
    ):

    if os.path.isfile(os.path.expandvars(filename)):
        try:
            import pypandoc
            long_description = pypandoc.convert_file(filename, "rst")
        except ImportError:
            long_description = open(filename).read()
    else:
        long_description = ""
    return long_description

if __name__ == "__main__":
    main()
