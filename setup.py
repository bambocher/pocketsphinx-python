#!/usr/bin/env python
import os
import sys
from shutil import copy, copytree, ignore_patterns
from glob import glob

from distutils import log
from distutils.command.build import build as _build
try:
    from setuptools import setup, Extension
    from setuptools.command.install import install as _install
    from setuptools.command.bdist_egg import bdist_egg as _bdist_egg
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension
    from distutils.command.install import install as _install
    from distutils.command.bdist_egg import bdist_egg as _bdist_egg

if sys.platform.startswith('win'):
    from distutils.command.bdist_msi import bdist_msi as _bdist_msi
    from distutils.command.bdist_wininst import bdist_wininst as _bdist_wininst


def _find_vcvarsall(version):
    vsbase = msvc9compiler.VS_BASE % version
    productdir = None
    
    if version != 9.0:
        try:
            productdir = msvc9compiler.Reg.get_value(r"%s\Setup\VC" % vsbase,
                                       "productdir")
        except KeyError:
            log.debug("Unable to find productdir in registry")

    if not productdir or not os.path.isdir(productdir):
        toolskey = "VS%0.f0COMNTOOLS" % version
        toolsdir = os.environ.get(toolskey, None)

        if toolsdir and os.path.isdir(toolsdir):
            productdir = os.path.join(toolsdir, os.pardir, os.pardir, "VC")
            productdir = os.path.abspath(productdir)
            if not os.path.isdir(productdir):
                log.debug("%s is not a valid directory" % productdir)
                return None
        else:
            log.debug("Env var %s is not set or invalid" % toolskey)
    if not productdir:
        log.debug("No productdir found")
        return None
    vcvarsall = os.path.join(productdir, "vcvarsall.bat")
    if os.path.isfile(vcvarsall):
        return vcvarsall
    log.debug("Unable to find vcvarsall.bat")
    return None


try:
    from distutils import msvc9compiler
    msvc9compiler.find_vcvarsall = _find_vcvarsall
except ImportError:
    pass


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
    ['-modern', '-threads'] +
    ['-I' + h for h in sb_include_dirs] +
    ['-Ideps/sphinxbase/swig'] +
    ['-outdir', 'sphinxbase']
)

ps_swig_opts = (
    ['-modern', '-threads'] +
    ['-I' + h for h in sb_include_dirs + ps_include_dirs] +
    ['-Ideps/sphinxbase/swig'] +
    ['-outdir', 'pocketsphinx']
)

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'pocketsphinx/model')):
    copytree(os.path.join(os.path.dirname(__file__), 'deps/pocketsphinx/model/en-us'),
             os.path.join(os.path.dirname(__file__), 'pocketsphinx/model'),
             ignore=ignore_patterns('en-us-phone.lm.bin'))
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'pocketsphinx/data')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'pocketsphinx/data'))
    copy(os.path.join(os.path.dirname(__file__), 'deps/pocketsphinx/test/data/goforward.raw'),
         os.path.join(os.path.dirname(__file__), 'pocketsphinx/data/goforward.raw'))


class build(_build):
    def run(self):
        self.run_command('build_ext')
        return _build.run(self)


class install(_install):
    def run(self):
        self.run_command('build_ext')
        return _install.run(self)


class bdist_egg(_bdist_egg):
    def run(self):
        self.run_command('build_ext')
        return _bdist_egg.run(self)


cmdclass = {
    'build': build,
    'install': install,
    'bdist_egg': bdist_egg
}


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    pass
else:
    class bdist_wheel(_bdist_wheel):
        def run(self):
            self.run_command('build_ext')
            return _bdist_wheel.run(self)

    cmdclass['bdist_wheel'] = bdist_wheel


if sys.platform.startswith('win'):
    class bdist_msi(_bdist_msi):
        def run(self):
            self.run_command('build_ext')
            return _bdist_msi.run(self)

    class bdist_wininst(_bdist_wininst):
        def run(self):
            self.run_command('build_ext')
            return _bdist_wininst.run(self)

    cmdclass['bdist_msi'] = bdist_msi
    cmdclass['bdist_wininst'] = bdist_wininst


setup(
    name='pocketsphinx',
    version='0.1.10',
    description='Python interface to CMU Sphinxbase and Pocketsphinx libraries',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dmitry Prazdnichnov',
    author_email='dp@bambucha.org',
    maintainer='Dmitry Prazdnichnov',
    maintainer_email='dp@bambucha.org',
    url='https://github.com/bambocher/pocketsphinx-python',
    download_url='https://pypi.org/project/pocketsphinx/#files',
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
    cmdclass=cmdclass,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Multimedia :: Sound/Audio :: Speech'
    ],
    license='BSD',
    keywords='sphinxbase pocketsphinx',
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
