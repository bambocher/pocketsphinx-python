#!/usr/bin/env python
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

libraries = []

libsphinxad = []

libsphinxbase = (
    glob('deps/sphinxbase/src/libsphinxbase/lm/*.c') +
    glob('deps/sphinxbase/src/libsphinxbase/feat/*.c') +
    glob('deps/sphinxbase/src/libsphinxbase/util/*.c') +
    glob('deps/sphinxbase/src/libsphinxbase/fe/*.c')
)

libpocketsphinx = glob('deps/pocketsphinx/src/libpocketsphinx/*.c')

sb_sources = (
    libsphinxbase +
    ['swig/sphinxbase/sphinxbase.i']
)

ps_sources = (
    libsphinxbase +
    libpocketsphinx +
    ['deps/pocketsphinx/swig/pocketsphinx.i']
)

sb_include_dirs = [
    'deps/sphinxbase/include',
    'deps/sphinxbase/include/sphinxbase'
]

ps_include_dirs = ['deps/pocketsphinx/include']

sb_swig_opts = (
    ['-modern'] +
    ['-I' + h for h in sb_include_dirs] +
    ['-Ideps/sphinxbase/swig'] +
    ['-outdir', 'sphinxbase']
)

ps_swig_opts = (
    ['-modern'] +
    ['-I' + h for h in sb_include_dirs] +
    ['-I' + h for h in ps_include_dirs] +
    ['-Ideps/sphinxbase/swig'] +
    ['-Iswig/sphinxbase'] +
    ['-outdir', 'pocketsphinx']
)

define_macros = [
    ('SPHINXBASE_EXPORTS', None),
    ('POCKETSPHINX_EXPORTS', None),
    ('SPHINX_DLL', None),
    ('HAVE_CONFIG_H', None)
]

extra_compile_args = []

if sys.platform.startswith('win'):
    libsphinxad.append('deps/sphinxbase/src/libsphinxad/ad_win32.c')
    sb_sources.extend(libsphinxad)
    sb_include_dirs.extend(['deps/sphinxbase/include/win32'])
    libraries.append('winmm')
    define_macros.extend([
        ('_WIN32', None),
        ('_CRT_SECURE_NO_DEPRECATE', None),
    ])
    extra_compile_args.extend([
        '/wd4244',
        '/wd4267',
        '/wd4197',
        '/wd4090',
        '/wd4018',
        '/wd4311',
        '/wd4312',
        '/wd4334'
    ])
elif sys.platform.startswith('darwin'):
    libsphinxad.append('deps/sphinxbase/src/libsphinxad/ad_oss.c')
    sb_sources.extend(libsphinxad)
    sb_include_dirs.extend(['deps/sphinxbase/include/android'])
    libraries.extend(['asound'])
else:
    sys.platform.startswith('linux')
    libsphinxad.append('deps/sphinxbase/src/libsphinxad/ad_pulse.c')
    sb_sources.extend(libsphinxad)
    sb_include_dirs.extend(['deps/sphinxbase/include/android'])
    libraries.extend(['pulse', 'pulse-simple'])
    extra_compile_args.extend([
        '-Wno-unused-label',
        '-Wno-strict-prototypes',
        '-Wno-parentheses',
        '-Wno-unused-but-set-variable',
        '-Wno-unused-variable',
        '-Wno-unused-result',
        '-Wno-sign-compare'
    ])

setup(
    name='pocketsphinx',
    version='0.1.1',
    description='Python interface to CMU SphinxBase and PocketSphinx libraries',
    long_description=open('README.rst').read(),
    author='Dmitry Prazdnichnov',
    author_email='dp@bambucha.org',
    maintainer='Dmitry Prazdnichnov',
    maintainer_email='dp@bambucha.org',
    url='https://github.com/bambocher/pocketsphinx-python',
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
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: C',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Sound/Audio :: Speech'
    ],
    license='BSD',
    keywords=['sphinxbase', 'pocketsphinx'],
    test_suite='tests',
    zip_safe=False
)
