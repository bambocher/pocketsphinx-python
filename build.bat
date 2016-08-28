@echo off

del /s /f /q venv2 venv3 build dist pocketsphinx.egg-info
del /s /f /q goforward.fsg goforward.htk goforward.lat
del /s /f /q sphinxbase/sphinxbase.py sphinxbase/*.pyd
del /s /f /q pocketsphinx/pocketsphinx.py pocketsphinx/*.pyd

"c:\Program Files (x86)\Python27\python.exe" setup.py sdist build
"c:\Program Files (x86)\Python27\python.exe" setup.py sdist upload

rem Python 2.7 x86

"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_egg build
"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_egg upload

"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_wininst build
"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_wininst upload

"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_msi build
"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_msi upload

"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_wheel build
"c:\Program Files (x86)\Python27\python.exe" setup.py bdist_wheel upload

rem Python 2.7 x64

"c:\Program Files\Python27\python.exe" setup.py bdist_egg build
"c:\Program Files\Python27\python.exe" setup.py bdist_egg upload

"c:\Program Files\Python27\python.exe" setup.py bdist_wininst build
"c:\Program Files\Python27\python.exe" setup.py bdist_wininst upload

"c:\Program Files\Python27\python.exe" setup.py bdist_msi build
"c:\Program Files\Python27\python.exe" setup.py bdist_msi upload

"c:\Program Files\Python27\python.exe" setup.py bdist_wheel build
"c:\Program Files\Python27\python.exe" setup.py bdist_wheel upload

rem Python 3.5 x86

"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_egg build
"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_egg upload

"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_wininst build
"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_wininst upload

"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_msi build
"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_msi upload

"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_wheel build
"c:\Program Files (x86)\Python35\python.exe" setup.py bdist_wheel upload

rem Python 3.5 x64

"c:\Program Files\Python35\python.exe" setup.py bdist_egg build
"c:\Program Files\Python35\python.exe" setup.py bdist_egg upload

"c:\Program Files\Python35\python.exe" setup.py bdist_wininst build
"c:\Program Files\Python35\python.exe" setup.py bdist_wininst upload

"c:\Program Files\Python35\python.exe" setup.py bdist_msi build
"c:\Program Files\Python35\python.exe" setup.py bdist_msi upload

"c:\Program Files\Python35\python.exe" setup.py bdist_wheel build
"c:\Program Files\Python35\python.exe" setup.py bdist_wheel upload

pause
