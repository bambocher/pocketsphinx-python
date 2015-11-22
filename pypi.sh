#!/usr/bin/env bash
rm -rf venv dist build *.egg-info
rm -rf ./sphinxbase/swig/python/sphinxbase.py
rm -rf ./pocketsphinx/swig/python/pocketsphinx.py

virtualenv -p /usr/bin/python2.7 venv
source venv/bin/activate
python setup.py bdist_egg build
python setup.py bdist_egg upload
python setup.py sdist build
python setup.py sdist --formats=gztar upload
python setup.py sdist --formats=zip upload
deactivate

rm -rf venv dist build *.egg-info
rm -rf ./sphinxbase/swig/python/sphinxbase.py
rm -rf ./pocketsphinx/swig/python/pocketsphinx.py

virtualenv -p /usr/bin/python3.5 venv
source venv/bin/activate
python setup.py bdist_egg build
python setup.py bdist_egg upload
deactivate

rm -rf venv dist build *.egg-info
rm -rf ./sphinxbase/swig/python/sphinxbase.py
rm -rf ./pocketsphinx/swig/python/pocketsphinx.py
