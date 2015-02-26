#!/usr/bin/env python
# encoding: utf-8
"""
Supported Platforms
-------------------

- Windows 7
- Windows 8
- Ubuntu 14.10

Dependencies
------------

* `Python <https://www.python.org/downloads/>`_
* `Swig <http://www.swig.org/download.html>`_
* `Microsoft Visual C++ Compiler for Python 2.7 <http://aka.ms/vcpython27>`_

Install
-------

.. code:: bash

    pip install PyPocketSphinx

or
--

.. code:: bash

    git clone https://github.com/bambocher/pocketsphinx-python.git
    cd pocketsphinx-python
    python setup.py install

Import
------

.. code:: python

    try:
        # Python 2.x
        from sphinxbase import Config
        from pocketsphinx import Decoder
    except ImportError:
        # Python 3.x
        from sphinxbase.sphinxbase import Config
        from pocketsphinx.pocketsphinx import Decoder
"""
import sys
from glob import glob
try:
    from setuptools import setup, Extension
    from distutils.command.build import build
    from setuptools.command.install import install
except Extension as err:
    from distutils.core import setup
    from distutils.extension import Extension
    from distutils.command.build import build
    from distutils.command.install import install

PY2 = sys.version_info[0] == 2

libsphinxbase = (
    [s for s in glob('sphinxbase/src/libsphinxbase/lm/*.c') if 'lm3g_templates.c' not in s] +
    glob('sphinxbase/src/libsphinxbase/feat/*.c') +
    glob('sphinxbase/src/libsphinxbase/util/*.c') +
    glob('sphinxbase/src/libsphinxbase/fe/*.c')
)

libsphinxad = []

libpocketsphinx = glob('pocketsphinx/src/libpocketsphinx/*.c')

sb_include_dirs = ['sphinxbase/include', 'sphinxbase/include/sphinxbase']
ps_include_dirs = ['pocketsphinx/include']

libraries = []

define_macros = [
    ('SPHINXBASE_EXPORTS', None),
    ('POCKETSPHINX_EXPORTS', None),
    ('HAVE_CONFIG_H', None),
    ('_CRT_SECURE_NO_DEPRECATE', None),
    ('_USRDLL', None),
    ('SPHINXDLL', None)
]

if sys.platform.startswith('linux'):
    libsphinxad.extend([
        'sphinxbase/src/libsphinxad/ad_oss.c'
    ])
    sb_include_dirs.extend(['include'])
elif sys.platform.startswith('win'):
    libsphinxad.extend([
        'sphinxbase/src/libsphinxad/ad_win32.c'
    ])
    sb_include_dirs.extend(['sphinxbase/include/win32'])
    libraries.append('winmm')
    define_macros.extend([
        ('WIN32', None),
        ('_WINDOWS', None),
        ('YY_NO_UNISTD_H', None)
    ])
elif sys.platform.startswith('darwin'):
    pass
else:
    pass

sb_sources = (
    libsphinxbase +
    libsphinxad +
    ['sphinxbase/swig/sphinxbase.i']
)

ps_sources = (
    libsphinxbase +
    libsphinxad +
    libpocketsphinx +
    ['pocketsphinx/swig/pocketsphinx.i']
)

swig_opts = ['-modern']

if not PY2:
    swig_opts.append('-py3')

sb_swig_opts = (
    swig_opts +
    ['-I' + h for h in sb_include_dirs] +
    ['-outdir', 'sphinxbase/swig/python']
)

ps_swig_opts = (
    swig_opts +
    ['-I' + h for h in sb_include_dirs] +
    ['-I' + h for h in ps_include_dirs] +
    ['-Isphinxbase/swig'] +
    ['-outdir', 'pocketsphinx/swig/python']
)

extra_compile_args = [
    '-Wno-unused-label',
    '-Wno-maybe-uninitialized',
    '-Wno-parentheses',
    '-Wno-unused-but-set-variable',
    '-Wno-unused-variable',
    '-Wno-unused-but-set-variable'
]

setup(
    name='pocketsphinx-python',
    version='0.0.1',
    description='Python interface to CMU SphinxBase and PocketSphinx libraries',
    long_description=__doc__,
    author='Dmitry Prazdnichnov',
    author_email='dp@bambucha.org',
    maintainer='Dmitry Prazdnichnov',
    maintainer_email='dp@bambucha.org',
    url='https://github.com/bambocher/pocketsphinx-python',
    download_url='https://pypi.python.org/pypi/PyPocketSphinx',
    packages=['sphinxbase', 'pocketsphinx'],
    ext_modules=[
        Extension(
            name='sphinxbase._sphinxbase',
            sources=sb_sources,
            swig_opts=sb_swig_opts,
            include_dirs=sb_include_dirs,
            libraries=libraries,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args
        ),
        Extension(
            name='pocketsphinx._pocketsphinx',
            sources=ps_sources,
            swig_opts=ps_swig_opts,
            include_dirs=sb_include_dirs + ps_include_dirs,
            libraries=libraries,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args
        )
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: C'
    ],
    license='BSD',
    keywords=['sphinxbase', 'pocketsphinx', 'PyPocketSphinx'],
    platforms=['Windows'],
    package_dir={
        'sphinxbase': 'sphinxbase/swig/python',
        'pocketsphinx': 'pocketsphinx/swig/python'
    }
)
