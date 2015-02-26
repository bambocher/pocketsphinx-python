#!/usr/bin/env bash

python2.7 setup.py bdist_egg upload
python3.4 setup.py bdist_egg upload
python2.7 setup.py bdist_wheel upload
python3.4 setup.py bdist_wheel upload
python2.7 setup.py sdist --formats=gztar upload
python2.7 setup.py sdist --formats=zip upload
