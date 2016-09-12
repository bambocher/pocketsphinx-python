*******************
Pocketsphinx Python
*******************

.. image:: https://img.shields.io/pypi/v/pocketsphinx.svg?maxAge=86400
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/pocketsphinx.svg?maxAge=86400
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: Development Status

.. image:: https://img.shields.io/pypi/pyversions/pocketsphinx.svg?maxAge=86400
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: Supported Python Versions

.. image:: https://travis-ci.org/bambocher/pocketsphinx-python.svg?branch=master
    :target: https://travis-ci.org/bambocher/pocketsphinx-python
    :alt: Build Status

.. image:: https://img.shields.io/pypi/l/pocketsphinx.svg?maxAge=86400
    :target: https://pypi.python.org/pypi/pocketsphinx
    :alt: License

Pocketsphinx is a part of the `CMU Sphinx <http://cmusphinx.sourceforge.net>`__ Open Source Toolkit For Speech Recognition.

This package provides a python interface to CMU `Sphinxbase <https://github.com/cmusphinx/sphinxbase>`__ and `Pocketsphinx <https://github.com/cmusphinx/pocketsphinx>`__ libraries created with `SWIG <http://www.swig.org>`__ and `Setuptools <https://setuptools.readthedocs.io>`__.

===================
Supported platforms
===================

* Windows
* Linux
* Mac OS X

============
Installation
============

.. code-block:: bash

    # Make sure we have up-to-date versions of pip, setuptools and wheel:
    $ pip install --upgrade pip setuptools wheel

    $ pip install --upgrade pocketsphinx

More binary distributions for manual installation are available `here <https://pypi.python.org/pypi/pocketsphinx>`__.

=====
Usage
=====

----------
LiveSpeech
----------

It's an iterator class for continuous recognition or keyword search from a microphone.

.. code-block:: python

    from pocketsphinx import LiveSpeech
    for phrase in LiveSpeech(): print(phrase)

An example of a keyword search:

.. code-block:: python

    from pocketsphinx import LiveSpeech

    speech = LiveSpeech(lm=False, keyphrase='forward', kws_threshold=1e+20)
    for phrase in speech:
        print(phrase.segments(detailed=True))

With your model and dictionary:

.. code-block:: python

    import os
    from pocketsphinx import LiveSpeech, get_model_path

    model_path = get_model_path()

    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'en-us'),
        lm=os.path.join(model_path, 'en-us.lm.bin'),
        dic=os.path.join(model_path, 'cmudict-en-us.dict')
    )

    for phrase in speech:
        print(phrase)

---------
AudioFile
---------

It's an iterator class for continuous recognition or keyword search from a file.

.. code-block:: python

    from pocketsphinx import AudioFile
    for phrase in AudioFile(): print(phrase) # => "go forward ten meters"

An example of a keyword search:

.. code-block:: python

    from pocketsphinx import AudioFile

    audio = AudioFile(lm=False, keyphrase='forward', kws_threshold=1e+20)
    for phrase in audio:
        print(phrase.segments(detailed=True)) # => "[('forward', -617, 63, 121)]"

With your model and dictionary:

.. code-block:: python

    import os
    from pocketsphinx import AudioFile, get_model_path, get_data_path

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'verbose': False,
        'audio_file': os.path.join(data_path, 'goforward.raw'),
        'buffer_size': 2048,
        'no_search': False,
        'full_utt': False,
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    audio = AudioFile(**config)
    for phrase in audio:
        print(phrase)

------------
Pocketsphinx
------------

It's a simple and flexible proxy class to `pocketsphinx.Decode`.

.. code-block:: python

    from pocketsphinx import Pocketsphinx
    print(Pocketsphinx().decode()) # => "go forward ten meters"

A more comprehensive example:

.. code-block:: python

    from __future__ import print_function
    import os
    from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

    model_path = get_model_path()
    data_path = get_data_path()

    config = {
        'hmm': os.path.join(model_path, 'en-us'),
        'lm': os.path.join(model_path, 'en-us.lm.bin'),
        'dict': os.path.join(model_path, 'cmudict-en-us.dict')
    }

    ps = Pocketsphinx(**config)
    ps.decode(
        audio_file=os.path.join(data_path, 'goforward.raw'),
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )

    print(ps.segments()) # => ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']
    print('Detailed segments:', *ps.segments(detailed=True), sep='\n') # => [
    #     word, prob, start_frame, end_frame
    #     ('<s>', 0, 0, 24)
    #     ('<sil>', -3778, 25, 45)
    #     ('go', -27, 46, 63)
    #     ('forward', -38, 64, 116)
    #     ('ten', -14105, 117, 152)
    #     ('meters', -2152, 153, 211)
    #     ('</s>', 0, 212, 260)
    # ]

    print(ps.hypothesis())  # => go forward ten meters
    print(ps.probability()) # => -32079
    print(ps.score())       # => -7066
    print(ps.confidence())  # => 0.04042641466841839

    print(*ps.best(count=10), sep='\n') # => [
    #     ('go forward ten meters', -28034)
    #     ('go for word ten meters', -28570)
    #     ('go forward and majors', -28670)
    #     ('go forward and meters', -28681)
    #     ('go forward and readers', -28685)
    #     ('go forward ten readers', -28688)
    #     ('go forward ten leaders', -28695)
    #     ('go forward can meters', -28695)
    #     ('go forward and leaders', -28706)
    #     ('go for work ten meters', -28722)
    # ]

--------------
Default config
--------------

If you don't pass any argument while creating an instance of the Pocketsphinx, AudioFile or LiveSpeech class, it will use next default values:

.. code-block:: python

    verbose = False
    logfn = /dev/null or nul
    audio_file = site-packages/pocketsphinx/data/goforward.raw
    audio_device = None
    sampling_rate = 16000
    buffer_size = 2048
    no_search = False
    full_utt = False
    hmm = site-packages/pocketsphinx/model/en-us
    lm = site-packages/pocketsphinx/model/en-us.lm.bin
    dict = site-packages/pocketsphinx/model/cmudict-en-us.dict

Any other option must be passed into the config as is, without using symbol `-`.

If you want to disable default language model or dictionary, you can change the value of the corresponding options to False:

.. code-block:: python

    lm = False
    dict = False

-------
Verbose
-------

Send output to stdout:

.. code-block:: python

    from pocketsphinx import Pocketsphinx

    ps = Pocketsphinx(verbose=True)
    ps.decode()

    print(ps.hypothesis())

Send output to file:

.. code-block:: python

    from pocketsphinx import Pocketsphinx

    ps = Pocketsphinx(verbose=True, logfn='pocketsphinx.log')
    ps.decode()

    print(ps.hypothesis())

-------------
Сompatibility
-------------

Parent classes are still available:

.. code-block:: python

    import os
    from pocketsphinx import DefaultConfig, Decoder, get_model_path, get_data_path

    model_path = get_model_path()
    data_path = get_data_path()

    # Create a decoder with a certain model
    config = DefaultConfig()
    config.set_string('-hmm', os.path.join(model_path, 'en-us'))
    config.set_string('-lm', os.path.join(model_path, 'en-us.lm.bin'))
    config.set_string('-dict', os.path.join(model_path, 'cmudict-en-us.dict'))
    decoder = Decoder(config)

    # Decode streaming data
    buf = bytearray(1024)
    with open(os.path.join(data_path, 'goforward.raw'), 'rb') as f:
        decoder.start_utt()
        while f.readinto(buf):
            decoder.process_raw(buf, False, False)
        decoder.end_utt()
    print('Best hypothesis segments:', [seg.word for seg in decoder.seg()])

===========================
Install development version
===========================

--------------------
Install requirements
--------------------

Windows requirements:

* `Python <https://www.python.org/downloads>`__
* `Git <http://git-scm.com/downloads>`__
* `Swig <http://www.swig.org/download.html>`__
* `Visual Studio Community <https://www.visualstudio.com/ru-ru/downloads/download-visual-studio-vs.aspx>`__

Ubuntu requirements:

.. code-block:: bash

    $ sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev

----------------
Install with pip
----------------

.. code-block:: bash

    $ pip install https://github.com/bambocher/pocketsphinx-python/archive/master.zip

----------------------
Install with distutils
----------------------

.. code-block:: bash

    $ git clone --recursive https://github.com/bambocher/pocketsphinx-python
    $ cd pocketsphinx-python
    $ python setup.py install

==================================
Projects using pocketsphinx-python
==================================

* `SpeechRecognition <https://github.com/Uberi/speech_recognition>`__ - Library for performing speech recognition, with support for several engines and APIs, online and offline.

=======
License
=======

`The BSD License <https://github.com/bambocher/pocketsphinx-python/blob/master/LICENSE>`__
