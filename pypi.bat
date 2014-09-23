@echo off

rmdir build /S /Q
rmdir dist /S /Q
rmdir PyPocketSphinx.egg-info /S /Q

del sphinxbase\swig\python\sphinxbase.py /F /Q
del sphinxbase\swig\sphinxbase_wrap.c /F /Q

del pocketsphinx\swig\python\pocketsphinx.py /F /Q
del pocketsphinx\swig\pocketsphinx_wrap.c /F /Q

C:\Python27\python.exe setup.py bdist_egg upload
C:\Python27_x64\python.exe setup.py bdist_egg upload
C:\Python34\python.exe setup.py bdist_egg upload
C:\Python34_x64\python.exe setup.py bdist_egg upload
C:\Python27\python.exe setup.py bdist_wininst upload
C:\Python27_x64\python.exe setup.py bdist_wininst upload
C:\Python34\python.exe setup.py bdist_wininst upload
C:\Python34_x64\python.exe setup.py bdist_wininst upload
C:\Python27\python.exe setup.py bdist_wheel upload
C:\Python34\python.exe setup.py bdist_wheel upload
C:\Python27\python.exe setup.py sdist --formats=gztar upload
C:\Python27\python.exe setup.py sdist --formats=zip upload
pause
