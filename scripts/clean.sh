#!/usr/bin/env bash
rm -rf build *.egg-info tests/*.{htk,lat}
rm -rf sphinxbase/{sphinxbase,pocketsphinx}.py {sphinxbase,pocketsphinx}/*.so
rm -rf pocketsphinx/{data,model}
