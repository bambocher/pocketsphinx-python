import unittest

import sphinxbase as sb
import pocketsphinx as ps


class TestConfig(unittest.TestCase):

    def test_config_get_float(self):
        config = ps.Decoder.default_config()
        f = config.get_float('-samprate')
        self.assertEqual(f, 16000.0)

    def test_config_set_float(self):
        config = ps.Decoder.default_config()
        config.set_float('-samprate', 8000.0)
        f = config.get_float('-samprate')
        self.assertEqual(f, 8000.0)

    def test_config_get_int(self):
        config = ps.Decoder.default_config()
        i = config.get_int('-nfft')
        self.assertEqual(i, 512)

    def test_config_set_int(self):
        config = ps.Decoder.default_config()
        config.set_int('-nfft', 256)
        i = config.get_int('-nfft')
        self.assertEqual(i, 256)

    def test_config_get_string(self):
        config = ps.Decoder.default_config()
        s = config.get_string('-rawlogdir')
        self.assertEqual(s, None)

    def test_config_set_string(self):
        config = ps.Decoder.default_config()
        config.set_string('-rawlogdir', '~/pocketsphinx')
        s = config.get_string('-rawlogdir')
        self.assertEqual(s, '~/pocketsphinx')

    def test_config_get_boolean(self):
        config = ps.Decoder.default_config()
        b = config.get_boolean('-backtrace')
        self.assertEqual(b, False)

    def test_config_set_boolean(self):
        config = ps.Decoder.default_config()
        config.set_boolean('-backtrace', True)
        b = config.get_boolean('-backtrace')
        self.assertEqual(b, True)
