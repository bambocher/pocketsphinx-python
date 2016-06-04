#!/usr/bin/env bash

rm -rf venv2 venv3 build dist pocketsphinx.egg-info
rm -rf sphinxbase/sphinxbase.py sphinxbase/*.so
rm -rf pocketsphinx/pocketsphinx.py pocketsphinx/*.so

virtualenv -p /usr/bin/python2.7 venv2
source venv2/bin/activate
python setup.py sdist build
python setup.py bdist_egg build
python setup.py bdist_wheel build
python setup.py sdist upload
python setup.py bdist_egg upload
python setup.py bdist_wheel upload
deactivate

virtualenv -p /usr/bin/python3.5 venv3
source venv3/bin/activate
python setup.py bdist_egg build
python setup.py bdist_wheel build
python setup.py bdist_egg upload
python setup.py bdist_wheel upload
deactivate
