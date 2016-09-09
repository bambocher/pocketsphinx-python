#!/usr/bin/env bash
rm -rf build dist *.egg-info tests/*.{htk,lat}
rm -rf sphinxbase/{sphinxbase,pocketsphinx}.py {sphinxbase,pocketsphinx}/*.so
rm -rf pocketsphinx/{data,model}

python setup.py sdist --formats=zip,gztar,bztar build
python2 setup.py bdist_egg build
python3 setup.py bdist_egg bdist_wheel build
