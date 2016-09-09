@echo off

rmdir /s /q build pocketsphinx.egg-info
rmdir /s /q sphinxbase\__pycache__ pocketsphinx\__pycache__ tests\__pycache__
rmdir /s /q pocketsphinx\data pocketsphinx\model
del /s /f /q sphinxbase\*.pyc pocketsphinx\*.pyc tests\*.pyc
del /s /f /q tests\*.htk tests\*.lat
del /s /f /q sphinxbase\sphinxbase.py sphinxbase\*.pyd
del /s /f /q pocketsphinx\pocketsphinx.py pocketsphinx\*.pyd
