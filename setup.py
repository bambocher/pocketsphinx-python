#!/usr/bin/env python
import os
import sys
from shutil import copy, copytree, rmtree, ignore_patterns
from glob import glob
try:
    from setuptools import setup, Extension
except:
    from distutils.core import setup
    from distutils.extension import Extension

extra_compile_args = []
extra_link_args = []
extra_objects = []
libraries = []

libsphinxbase = (
    glob('deps/sphinxbase/src/libsphinxbase/lm/*.c') +
    glob('deps/sphinxbase/src/libsphinxbase/feat/*.c') +
    glob('deps/sphinxbase/src/libsphinxbase/util/*.c') +
    glob('deps/sphinxbase/src/libsphinxbase/fe/*.c')
)

libpocketsphinx = glob('deps/pocketsphinx/src/libpocketsphinx/*.c')

ad_sources = ['swig/sphinxbase/ad.i']

sb_sources = (
    libsphinxbase +
    ['deps/sphinxbase/swig/sphinxbase.i']
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

define_macros = [
    ('SPHINXBASE_EXPORTS', None),
    ('POCKETSPHINX_EXPORTS', None),
    ('SPHINX_DLL', None),
    ('HAVE_CONFIG_H', None)
]

if sys.platform.startswith('win'):
    ad_sources.append('deps/sphinxbase/src/libsphinxad/ad_win32.c')
    sb_include_dirs.append('deps/sphinxbase/include/win32')
    libraries.append('winmm')
    extra_compile_args.extend([
        '/wd4244',
        '/wd4267',
        '/wd4197',
        '/wd4090',
        '/wd4018',
        '/wd4311',
        '/wd4312',
        '/wd4334',
        '/wd4477',
        '/wd4996'
    ])
    extra_link_args.append('/ignore:4197')
elif sys.platform.startswith('darwin'):
    ad_sources.append('deps/sphinxbase/src/libsphinxad/ad_openal.c')
    sb_include_dirs.extend([
        '/System/Library/Frameworks/OpenAL.framework/Versions/A/Headers',
        'deps/sphinxbase/include/android'
    ])
    extra_objects.extend([
        '/System/Library/Frameworks/OpenAL.framework/Versions/A/OpenAL'
    ])
    extra_compile_args.extend([
        '-Wno-macro-redefined',
        '-Wno-sign-compare',
        '-Wno-logical-op-parentheses'
    ])
elif sys.platform.startswith('linux'):
    ad_sources.append('deps/sphinxbase/src/libsphinxad/ad_pulse.c')
    sb_include_dirs.append('deps/sphinxbase/include/android')
    libraries.extend(['pulse', 'pulse-simple'])
    extra_compile_args.extend([
        '-Wno-unused-label',
        '-Wno-strict-prototypes',
        '-Wno-parentheses',
        '-Wno-unused-but-set-variable',
        '-Wno-unused-variable',
        '-Wno-unused-result',
        '-Wno-sign-compare',
        '-Wno-misleading-indentation'
    ])

sb_swig_opts = (
    ['-modern'] +
    ['-I' + h for h in sb_include_dirs] +
    ['-Ideps/sphinxbase/swig'] +
    ['-outdir', 'sphinxbase']
)

ps_swig_opts = (
    ['-modern'] +
    ['-I' + h for h in sb_include_dirs + ps_include_dirs] +
    ['-Ideps/sphinxbase/swig'] +
    ['-outdir', 'pocketsphinx']
)

rmtree('pocketsphinx/data', True)
rmtree('pocketsphinx/model', True)
copytree('deps/pocketsphinx/model/en-us',
         'pocketsphinx/model',
         ignore=ignore_patterns('en-us-phone.lm.bin'))
os.makedirs('pocketsphinx/data')
copy('deps/pocketsphinx/test/data/goforward.raw',
     'pocketsphinx/data/goforward.raw')

setup(
    name='pocketsphinx',
    version='0.1.1',
    description='Python interface to CMU Sphinxbase and Pocketsphinx libraries',
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
            name='sphinxbase._ad',
            sources=ad_sources,
            swig_opts=sb_swig_opts,
            include_dirs=sb_include_dirs,
            extra_objects=extra_objects,
            libraries=libraries,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        ),
        Extension(
            name='sphinxbase._sphinxbase',
            sources=sb_sources,
            swig_opts=sb_swig_opts,
            include_dirs=sb_include_dirs,
            extra_objects=extra_objects,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        ),
        Extension(
            name='pocketsphinx._pocketsphinx',
            sources=ps_sources,
            swig_opts=ps_swig_opts,
            include_dirs=sb_include_dirs + ps_include_dirs,
            extra_objects=extra_objects,
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args
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
    include_package_data=True,
    zip_safe=False
)
