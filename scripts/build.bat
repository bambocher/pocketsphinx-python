@echo off

set python27_x64="c:\Program Files\Python27\python.exe"
set python35_x64="c:\Program Files\Python35\python.exe"
set python27_x86="c:\Program Files (x86)\Python27\python.exe"
set python35_x86="c:\Program Files (x86)\Python35\python.exe"

rmdir /s /q dist

call scripts\clean.bat
%python27_x86% setup.py sdist --formats=zip,gztar,bztar

call scripts\clean.bat
%python27_x86% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python27_x86% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build

call scripts\clean.bat
%python27_x64% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python27_x64% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build

call scripts\clean.bat
%python35_x86% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python35_x86% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build

call scripts\clean.bat
%python35_x64% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build
%python35_x64% setup.py bdist_egg bdist_wininst bdist_msi bdist_wheel build

pause
