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

    pip install pocketsphinx

or
--

.. code:: bash

    git clone https://github.com/bambocher/pocketsphinx-python.git
    cd pocketsphinx-python
    python setup.py install

Import
------

.. code:: python

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
    glob('sphinxbase/src/libsphinxbase/lm/*.c') +
    glob('sphinxbase/src/libsphinxbase/feat/*.c') +
    glob('sphinxbase/src/libsphinxbase/util/*.c') +
    glob('sphinxbase/src/libsphinxbase/fe/*.c')
)

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

extra_compile_args = []

if sys.platform.startswith('linux'):
    sb_include_dirs.extend(['include'])
    extra_compile_args.extend([
        '-Wno-unused-label',
        '-Wno-maybe-uninitialized',
        '-Wno-parentheses',
        '-Wno-unused-but-set-variable',
        '-Wno-unused-variable'
    ])
elif sys.platform.startswith('win'):
    sb_include_dirs.extend(['sphinxbase/include/win32'])
    define_macros.extend([
        ('WIN32', None),
        ('_WINDOWS', None),
        ('YY_NO_UNISTD_H', None)
    ])
    extra_compile_args.extend([
        '/wd4244',
        '/wd4267',
        '/wd4197',
        '/wd4090',
        '/wd4018'
    ])
elif sys.platform.startswith('darwin'):
    sb_include_dirs.extend(['include'])
else:
    pass

sb_sources = (
    libsphinxbase +
    ['sphinxbase/swig/sphinxbase.i']
)

ps_sources = (
    libsphinxbase +
    libpocketsphinx +
    ['pocketsphinx/swig/pocketsphinx.i']
)

swig_opts = ['-modern']

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

setup(
    name='pocketsphinx',
    version='0.0.5',
    description='Python interface to CMU SphinxBase and PocketSphinx libraries',
    long_description=__doc__,
    author='Dmitry Prazdnichnov',
    author_email='dp@bambucha.org',
    maintainer='Dmitry Prazdnichnov',
    maintainer_email='dp@bambucha.org',
    url='https://github.com/cmusphinx/pocketsphinx-python',
    download_url='https://pypi.python.org/pypi/pocketsphinx',
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
    keywords=['sphinxbase', 'pocketsphinx'],
    platforms=['Windows'],
    package_dir={
        'sphinxbase': 'sphinxbase/swig/python',
        'pocketsphinx': 'pocketsphinx/swig/python'
    }
)
