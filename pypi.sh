#!/usr/bin/env bash

virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
python setup.py bdist_egg upload
python setup.py bdist_wheel upload
python setup.py sdist --formats=gztar upload
python setup.py sdist --formats=zip upload
deactivate

virtualenv -p /usr/bin/python3.5 venv
source venv/bin/activate
python setup.py bdist_egg upload
python setup.py bdist_wheel upload
python setup.py sdist --formats=gztar upload
python setup.py sdist --formats=zip upload
deactivate
