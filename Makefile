ifeq ($(OS),Windows_NT)
	PYTHON2_X86 = "c:\Program Files (x86)\Python27\python.exe"
	PYTHON3_X86 = "c:\Program Files (x86)\Python35\python.exe"
	PYTHON2_X64 = "c:\Program Files\Python27\python.exe"
	PYTHON3_X64 = "c:\Program Files\Python35\python.exe"
else
	PYTHON2_X86 = python2
	PYTHON3_X86 = python3
	PYTHON2_X64 = python2
	PYTHON3_X64 = python3
endif

.PHONY: all build upload test clean

all: build

ifeq ($(OS),Windows_NT)
build: build_sdist \
	build_egg_py2_x86 \
	build_egg_py3_x86 \
	build_egg_py2_x64 \
	build_egg_py3_x64 \
	build_wheel_py2_x86 \
	build_wheel_py3_x86 \
	build_wheel_py2_x64 \
	build_wheel_py3_x64 \
	build_wininst_py2_x86 \
	build_wininst_py3_x86 \
	build_wininst_py2_x64 \
	build_wininst_py3_x64 \
	build_msi_py2_x86 \
	build_msi_py3_x86 \
	build_msi_py2_x64 \
	build_msi_py3_x64
else
build: build_sdist \
	build_egg_py2_x64 \
	build_egg_py3_x64 \
	build_wheel_py2_x64 \
	build_wheel_py3_x64
endif

build_sdist: clean
	$(PYTHON2_X86) setup.py sdist --formats=zip,gztar,bztar

build_egg_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_egg build

build_egg_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_egg build

build_egg_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_egg build

build_egg_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_egg build

build_wheel_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_wheel build

build_wheel_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_wheel build

build_wheel_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_wheel build

build_wheel_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_wheel build

build_msi_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_msi build

build_msi_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_msi build

build_msi_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_msi build

build_msi_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_msi build

build_wininst_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_wininst build

build_wininst_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_wininst build

build_wininst_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_wininst build

build_wininst_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_wininst build

ifeq ($(OS),Windows_NT)
upload: upload_sdist \
	upload_egg_py2_x86 \
	upload_egg_py3_x86 \
	upload_egg_py2_x64 \
	upload_egg_py3_x64 \
	upload_wheel_py2_x86 \
	upload_wheel_py3_x86 \
	upload_wheel_py2_x64 \
	upload_wheel_py3_x64 \
	upload_wininst_py2_x86 \
	upload_wininst_py3_x86 \
	upload_wininst_py2_x64 \
	upload_wininst_py3_x64 \
	upload_msi_py2_x86 \
	upload_msi_py3_x86 \
	upload_msi_py2_x64 \
	upload_msi_py3_x64
else
upload: upload_sdist \
	upload_egg_py2_x64 \
	upload_egg_py3_x64
endif

upload_sdist: clean
	$(PYTHON2_X86) setup.py sdist --formats=zip,gztar,bztar upload

upload_egg_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_egg upload

upload_egg_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_egg upload

upload_egg_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_egg upload

upload_egg_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_egg upload

upload_wheel_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_wheel upload

upload_wheel_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_wheel upload

upload_wheel_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_wheel upload

upload_wheel_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_wheel upload

upload_msi_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_msi upload

upload_msi_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_msi upload

upload_msi_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_msi upload

upload_msi_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_msi upload

upload_wininst_py2_x86: clean
	$(PYTHON2_X86) setup.py bdist_wininst upload

upload_wininst_py3_x86: clean
	$(PYTHON3_X86) setup.py bdist_wininst upload

upload_wininst_py2_x64: clean
	$(PYTHON2_X64) setup.py bdist_wininst upload

upload_wininst_py3_x64: clean
	$(PYTHON3_X64) setup.py bdist_wininst upload

ifeq ($(OS),Windows_NT)
test: test_py2_x86 test_py2_x64 test_py3_x86 test_py3_x64
else
test: test_py2_x64 test_py3_x64
endif

test_py2_x86: clean
	$(PYTHON2_X86) setup.py test

test_py3_x86: clean
	$(PYTHON3_X86) setup.py test

test_py2_x64: clean
	$(PYTHON2_X64) setup.py test

test_py3_x64: clean
	$(PYTHON3_X64) setup.py test

clean:
	rm -rf build *.egg-info tests/*.{htk,lat}
	rm -rf sphinxbase/{ad,sphinxbase}.py
	rm -rf pocketsphinx/pocketsphinx.py
	rm -rf {sphinxbase,pocketsphinx}/*.{so,pyd}
	rm -rf {sphinxbase,pocketsphinx,tests}/*.pyc
	rm -rf {sphinxbase,pocketsphinx,tests}/__pycache__
	rm -rf pocketsphinx/{data,model}
	rm -rf swig/sphinxbase/*.c
	rm -rf deps/{sphinxbase,pocketsphinx}/swig/*.c

