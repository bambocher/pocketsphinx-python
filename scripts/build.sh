#!/usr/bin/env bash

rm -rf dist

scripts/clean.sh
python setup.py sdist --formats=zip,gztar,bztar

scripts/clean.sh
python2 setup.py bdist_egg build
python2 setup.py bdist_egg build

scripts/clean.sh
python3 setup.py bdist_egg bdist_wheel build
python3 setup.py bdist_egg bdist_wheel build
