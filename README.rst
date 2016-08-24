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

* Windows 7
* Windows 8
* Windows 10
* Ubuntu 14.04

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
    $ sudo apt-get install -qq python python-dev python-pip build-essential swig libpulse-dev
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

    #!/usr/bin/env python
    import os

    import sphinxbase as sb
    import pocketsphinx as ps

    MODELDIR = 'deps/pocketsphinx/model'
    DATADIR = 'deps/pocketsphinx/test/data'

    # Create a decoder with certain model
    config = ps.Decoder.default_config()
    config.set_string('-hmm', os.path.join(MODELDIR, 'en-us/en-us'))
    config.set_string('-lm', os.path.join(MODELDIR, 'en-us/en-us.lm.bin'))
    config.set_string('-dict', os.path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
    decoder = ps.Decoder(config)

    # Decode streaming data.
    decoder.start_utt()
    stream = open(os.path.join(DATADIR, 'goforward.raw'), 'rb')
    while True:
        buf = stream.read(1024)
        if buf:
            decoder.process_raw(buf, False, False)
        else:
            break
    decoder.end_utt()
    stream.close()
    print('Best hypothesis segments:', [seg.word for seg in decoder.seg()])

==================================
Projects using pocketsphinx-python
==================================

* `SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ - Library for performing speech recognition, with support for several engines and APIs, online and offline.

=======
License
=======

`The BSD License <https://github.com/bambocher/pocketsphinx-python/blob/master/LICENSE>`__
