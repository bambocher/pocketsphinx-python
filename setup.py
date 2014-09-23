#!/usr/bin/env python
# encoding: utf-8
import os
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

libsphinxbase = (
    [s for s in glob('sphinxbase/src/libsphinxbase/lm/*.c') if 'lm3g_templates.c' not in s] +
    glob('sphinxbase/src/libsphinxbase/feat/*.c') +
    glob('sphinxbase/src/libsphinxbase/util/*.c') +
    glob('sphinxbase/src/libsphinxbase/fe/*.c')
)

libsphinxad = []

libpocketsphinx = glob('pocketsphinx/src/libpocketsphinx/*.c')

sb_headers = ['sphinxbase/include', 'sphinxbase/include/win32']
ps_headers = ['pocketsphinx/include', 'sphinxbase/src/libpocketsphinx']

libraries = []

definitions = [
    ('SPHINXBASE_EXPORTS', None),
    ('POCKETSPHINX_EXPORTS', None),
    ('HAVE_CONFIG_H', None),
    ('_CRT_SECURE_NO_DEPRECATE', None),
    ('_USRDLL', None),
    ('SPHINXDLL', None)
]

if sys.platform.startswith('linux'):
    pass
elif sys.platform.startswith('win'):
    libsphinxad.extend(['sphinxbase/src/libsphinxad/play_win32.c', 'sphinxbase/src/libsphinxad/rec_win32.c'])
    libraries.append('winmm')
    definitions.extend([('WIN32', None), ('_WINDOWS', None), ('YY_NO_UNISTD_H', None)])
elif sys.platform.startswith('darwin'):
    pass
elif sys.platform == 'cygwin':
      libraries.append('iconv')


class Build(build):
    def run(self):
        self.run_command('build_ext')
        build.run(self)


class Install(install):
    def run(self):
        self.run_command('build_ext')
        install.run(self)


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name = 'PyPocketSphinx',
    version = '12608',
    description = 'Python interface to CMU SphinxBase and PocketSphinx libraries',
    long_description = read('readme.md'),
    author = 'Dmitry Prazdnichnov',
    author_email = 'dp@bambucha.org',
    maintainer = '',
    maintainer_email = '',
    url = 'https://github.com/bambocher/PyPocketSphinx',
    download_url = '',
    packages = ['sphinxbase', 'pocketsphinx'],
    ext_modules = [
        Extension(
            name = 'sphinxbase._sphinxbase',
            sources = libsphinxbase + libsphinxad + ['sphinxbase/swig/sphinxbase.i'],
            swig_opts = ['-modern'] + ['-I' + h for h in sb_headers] + ['-outdir', 'sphinxbase/swig/python'],
            include_dirs = sb_headers,
            libraries = libraries,
            define_macros = definitions
        ),
        Extension(
            name = 'pocketsphinx._pocketsphinx',
            sources = libsphinxbase + libsphinxad + libpocketsphinx + ['pocketsphinx/swig/pocketsphinx.i'],
            swig_opts = ['-modern'] + ['-I' + h for h in sb_headers] + ['-I' + h for h in ps_headers] + ['-Isphinxbase/swig'] + ['-outdir', 'pocketsphinx/swig/python'],
            include_dirs = sb_headers + ps_headers,
            libraries = libraries,
            define_macros = definitions
        )
    ],
    cmdclass = {'build': Build, 'install': Install},
    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    license = 'BSD',
    keywords = ['sphinxbase', 'pocketsphinx'],
    platforms = ['Windows'],
    package_dir = {
        'sphinxbase': 'sphinxbase/swig/python',
        'pocketsphinx': 'pocketsphinx/swig/python'
    }
)
