#!/usr/bin/env bash

rm -rf dist

scrips/clean.sh
python setup.py sdist --formats=zip,gztar,bztar upload

scrips/clean.sh
python2 setup.py bdist_egg build
python2 setup.py bdist_egg upload

scrips/clean.sh
python3 setup.py bdist_egg bdist_wheel build
python3 setup.py bdist_egg bdist_wheel upload
