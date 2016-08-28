*******************
Pocketsphinx Python
*******************

.. image:: https://img.shields.io/pypi/v/pocketsphinx.svg
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/pocketsphinx.svg
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: Development Status

.. image:: https://img.shields.io/pypi/pyversions/pocketsphinx.svg
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: Supported Python Versions

.. image:: https://travis-ci.org/bambocher/pocketsphinx-python.svg?branch=master
    :target: https://travis-ci.org/bambocher/pocketsphinx-python
    :alt: Build Status

.. image:: https://img.shields.io/pypi/l/pocketsphinx.svg
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: License

Python interface to CMU `Sphinxbase <https://github.com/cmusphinx/sphinxbase>`__ and `Pocketsphinx <https://github.com/cmusphinx/pocketsphinx>`__ libraries created with `SWIG <http://www.swig.org>`__.
Pocketsphinx packages include python support, however, it is based on Automake and not well supported on Windows.
Pocketsphinx is part of the `CMU Sphinx <http://cmusphinx.sourceforge.net>`__ Open Source Toolkit For Speech Recognition.

This package provides module created with Python distutils setup and can be more portable.

===================
Supported Platforms
===================

* Windows
* Linux
* Mac OS X

===================
Install on Windows
===================

------------
Requirements
------------

* `Python <https://www.python.org/downloads>`__
* `Git <http://git-scm.com/downloads>`__
* `Swig <http://www.swig.org/download.html>`__
* `Visual Studio Community <https://www.visualstudio.com/ru-ru/downloads/download-visual-studio-vs.aspx>`__

-------
Install
-------

.. code-block:: bash

    # From pip
    $ pip install pocketsphinx

    # From source
    $ git clone --recursive https://github.com/bambocher/pocketsphinx-python
    $ cd pocketsphinx-python
    $ python setup.py install

=================
Install on Ubuntu
=================

------------
Requirements
------------

* python
* python-dev
* python-pip
* build-essential
* swig
* git
* libpulse-dev

-------
Install
-------

.. code-block:: bash

    # From pip
    $ sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev
    $ sudo pip install pocketsphinx

    # From source
    $ sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev
    $ git clone --recursive https://github.com/bambocher/pocketsphinx-python
    $ cd pocketsphinx-python
    $ sudo python setup.py install

===========
Basic usage
===========

.. code-block:: python

    from pocketsphinx import Pocketsphinx

    ps = Pocketsphinx()
    ps.decode()

    print(ps.segments())
    # ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']

    print(ps.hypothesis())
    # go forward ten meters

    print(ps.probability())
    # -32079

    print(ps.score())
    # -7066

    print(ps.confidence())
    # 0.04042641466841839

    print(*ps.best(), sep='\n')
    # ('go forward ten meters', -28034)
    # ('go for word ten meters', -28570)
    # ('go forward and majors', -28670)
    # ('go forward and meters', -28681)
    # ('go forward and readers', -28685)
    # ('go forward ten readers', -28688)
    # ('go forward ten leaders', -28695)
    # ('go forward can meters', -28695)
    # ('go forward and leaders', -28706)
    # ('go for work ten meters', -28722)

==================================
Projects using pocketsphinx-python
==================================

* `SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ - Library for performing speech recognition, with support for several engines and APIs, online and offline.

=======
License
=======

`The BSD License <https://github.com/bambocher/pocketsphinx-python/blob/master/LICENSE>`__
