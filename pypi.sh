#!/usr/bin/env bash

python2 setup.py bdist_egg upload
python3 setup.py bdist_egg upload
python2 setup.py bdist_wheel upload
python3 setup.py bdist_wheel upload
python2 setup.py sdist --formats=gztar upload
python2 setup.py sdist --formats=zip upload
