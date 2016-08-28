#!/usr/bin/env python
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
    libsphinxbase
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
    if os.environ.get('ENABLE_LIBSPHINXAD'):
        libsphinxad.append('deps/sphinxbase/src/libsphinxad/ad_win32.c')
        sb_sources.extend(libsphinxad)
        sb_sources.extend(['swig/sphinxbase/sphinxbase.i'])
        ps_swig_opts.extend(['-Iswig/sphinxbase'])
        libraries.append('winmm')
    else:
        sb_sources.extend(['deps/sphinxbase/swig/sphinxbase.i'])
    sb_include_dirs.extend(['deps/sphinxbase/include/win32'])
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
    sb_include_dirs.extend(['deps/sphinxbase/include/android'])
else:
    sys.platform.startswith('linux')
    if os.environ.get('ENABLE_LIBSPHINXAD'):
        libsphinxad.append('deps/sphinxbase/src/libsphinxad/ad_pulse.c')
        sb_sources.extend(libsphinxad)
        sb_sources.extend(['swig/sphinxbase/sphinxbase.i'])
        ps_swig_opts.extend(['-Iswig/sphinxbase'])
        libraries.extend(['pulse', 'pulse-simple'])
    else:
        sb_sources.extend(['deps/sphinxbase/swig/sphinxbase.i'])
    sb_include_dirs.extend(['deps/sphinxbase/include/android'])
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
    data_files=[
        ('pocketsphinx/data', ['deps/pocketsphinx/test/data/goforward.raw']),
        ('pocketsphinx/model', [
            'deps/pocketsphinx/model/en-us/cmudict-en-us.dict',
            'deps/pocketsphinx/model/en-us/en-us.lm.bin'
        ]),
        ('pocketsphinx/model/en-us', [
            'deps/pocketsphinx/model/en-us/en-us/README',
            'deps/pocketsphinx/model/en-us/en-us/feat.params',
            'deps/pocketsphinx/model/en-us/en-us/mdef',
            'deps/pocketsphinx/model/en-us/en-us/means',
            'deps/pocketsphinx/model/en-us/en-us/noisedict',
            'deps/pocketsphinx/model/en-us/en-us/sendump',
            'deps/pocketsphinx/model/en-us/en-us/transition_matrices',
            'deps/pocketsphinx/model/en-us/en-us/variances'
        ])
    ],
    zip_safe=False
)
