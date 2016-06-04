*******************
pocketsphinx-python
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

Python interface to CMU SphinxBase and PocketSphinx libraries created with SWIG.
Pocketsphinx packages include python support, however, it is based on Automake and not well supported on Windows.

This package provides module created with Python distutils setup and can be more portable.

===================
Supported Platforms
===================

* Windows 7
* Windows 8
* Ubuntu 14.04

===================
Install on Windows
===================

------------
Requirements
------------

* `Python <http://aka.ms/vcpython27>`__
* `git <http://git-scm.com/downloads>`__
* `Swig <http://www.swig.org/download.html>`__
* `Microsoft Visual C++ Compiler for Python 2.7 <http://aka.ms/vcpython27>`__

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

-------
Install
-------

.. code-block:: bash

    # From pip
    $ sudo apt-get install -qq python python-dev python-pip build-essential swig
    $ sudo pip install pocketsphinx

    # From source
    $ sudo apt-get install -qq python python-dev python-pip build-essential swig git
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
    config.set_string('-logfn', '/dev/null')
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

=======
License
=======

`The BSD License <https://github.com/bambocher/pocketsphinx-python/blob/master/LICENSE>`__
