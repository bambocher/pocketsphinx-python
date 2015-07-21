pocketsphinx-python
===================

Python interface to CMU SphinxBase and PocketSphinx libraries created with SWIG.
Pocketsphinx packages include python support, however, it is based on Automake and
not well supported on Windows.

This package provides module created with Python distutils setup and can be more
portable.

Supported Platforms
-------------------

- Windows 7
- Windows 8
- Ubuntu 14.10

Install on Windows
------------------

### Dependencies

- [Python](https://www.python.org/downloads/)
- [git](http://git-scm.com/downloads)
- [pip](https://pypi.python.org/pypi/pip/)
- [Swig](http://www.swig.org/download.html)
- [Microsoft Visual C++ Compiler for Python 2.7](http://aka.ms/vcpython27)

### Install

```bash
pip install pocketsphinx
```

or

```bash
git clone --recursive https://github.com/bambocher/pocketsphinx-python
cd pocketsphinx-python
python setup.py install
```

Install on Ubuntu
-----------------

### Dependencies

- python
- python-dev
- python-pip
- build-essential
- swig
- git

### Install

```bash
sudo apt-get install -y python python-dev python-pip build-essential swig git
sudo pip install pocketsphinx
```

or

```bash
sudo apt-get install -y python python-dev python-pip build-essential swig git
git clone --recursive https://github.com/bambocher/pocketsphinx-python
cd pocketsphinx-python
sudo python setup.py install
```

Basic usage
-----------

```python
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *

MODELDIR = "pocketsphinx/model"
DATADIR = "pocketsphinx/test/data"

# Create a decoder with certain model
config = Decoder.default_config()
config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
decoder = Decoder(config)

# Decode streaming data.
decoder = Decoder(config)
decoder.start_utt()
stream = open(path.join(DATADIR, 'goforward.raw'), 'rb')
while True:
  buf = stream.read(1024)
  if buf:
    decoder.process_raw(buf, False, False)
  else:
    break
decoder.end_utt()
print ('Best hypothesis segments: ', [seg.word for seg in decoder.seg()])
```
