pocketsphinx-python
===================

Python interface to CMU SphinxBase and PocketSphinx libraries

Supported Platforms
-------------------

- Windows 7
- Windows 8
- Ubuntu 14.10

Install on Windows
------------------

### Dependencies

- [Python](https://www.python.org/downloads/)
- [Swig](http://www.swig.org/download.html)
- [Microsoft Visual C++ Compiler for Python 2.7](http://aka.ms/vcpython27)

### Install

```bash
pip install PyPocketSphinx
```

or

```bash
git clone --recursive https://github.com/bambocher/pocketsphinx-python
cd pocketsphinx-python
python setup.py install
```

### Import

```python
try:
    # Python 2.x
    from sphinxbase import Config
    from pocketsphinx import Decoder
except ImportError:
    # Python 3.x
    from sphinxbase.sphinxbase import Config
    from pocketsphinx.pocketsphinx import Decoder
```
