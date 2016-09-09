@echo off

rmdir /s /q build dist pocketsphinx.egg-info
rmdir /s /q sphinxbase\__pycache__ pocketsphinx\__pycache__ tests\__pycache__
rmdir /s /q pocketsphinx\data pocketsphinx\model
del /s /f /q sphinxbase\*.pyc pocketsphinx\*.pyc tests\*.pyc
del /s /f /q tests\*.htk tests\*.lat
del /s /f /q sphinxbase\sphinxbase.py sphinxbase\*.pyd
del /s /f /q pocketsphinx\pocketsphinx.py pocketsphinx\*.pyd

set python27_x64="c:\Program Files\Python27\python.exe"
set python35_x64="c:\Program Files\Python35\python.exe"
set python27_x86="c:\Program Files (x86)\Python27\python.exe"
set python35_x86="c:\Program Files (x86)\Python35\python.exe"

%python27_x86% setup.py sdist --formats=zip,gztar,bztar build
%python27_x86% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python27_x64% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python35_x86% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python35_x64% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build

pause
