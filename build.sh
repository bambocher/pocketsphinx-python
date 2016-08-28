#!/usr/bin/env bash
rm -rf venv2 venv3 build dist *.egg-info tests/*.{htk,lat}
rm -rf sphinxbase/{sphinxbase,pocketsphinx}.py {sphinxbase,pocketsphinx}/*.so

python setup.py sdist --formats=zip,gztar,bztar build
#python setup.py sdist --formats=zip,gztar,bztar upload

virtualenv -p /usr/bin/python2.7 venv2
source venv2/bin/activate
python setup.py bdist_egg build
#python setup.py bdist_egg upload
python setup.py bdist_wheel build
#python setup.py bdist_wheel upload
deactivate

virtualenv -p /usr/bin/python3.5 venv3
source venv3/bin/activate
python setup.py bdist_egg build
#python setup.py bdist_egg upload
python setup.py bdist_wheel build
#python setup.py bdist_wheel upload
deactivate
