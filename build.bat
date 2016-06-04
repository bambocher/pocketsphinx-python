@echo off

C:\Python27\python.exe setup.py bdist_egg upload
C:\Python27_x64\python.exe setup.py bdist_egg upload
C:\Python34\python.exe setup.py bdist_egg upload
C:\Python34_x64\python.exe setup.py bdist_egg upload
C:\Python27\python.exe setup.py bdist_wininst upload
C:\Python27_x64\python.exe setup.py bdist_wininst upload
C:\Python34\python.exe setup.py bdist_wininst upload
C:\Python34_x64\python.exe setup.py bdist_wininst upload
C:\Python27\python.exe setup.py bdist_msi upload
C:\Python27_x64\python.exe setup.py bdist_msi upload
C:\Python34\python.exe setup.py bdist_msi upload
C:\Python34_x64\python.exe setup.py bdist_msi upload
C:\Python27\python.exe setup.py bdist_wheel upload
C:\Python34\python.exe setup.py bdist_wheel upload
C:\Python27\python.exe setup.py sdist --formats=gztar upload
C:\Python27\python.exe setup.py sdist --formats=zip upload
pause
