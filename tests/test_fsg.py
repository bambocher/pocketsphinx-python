import unittest

import sphinxbase as sb


class TestFsg(unittest.TestCase):

    def test_fsg_word_add(self):
        log_math = sb.LogMath()
        fsg_model = sb.FsgModel('simple_grammar', log_math, 1.0, 10)
        fsg_model.word_add('hello')
        fsg_model.word_add('world')
        word_id = fsg_model.word_id('world')
        self.assertGreaterEqual(word_id, 0)

    def test_fsg_add_silence(self):
        log_math = sb.LogMath()
        fsg_model = sb.FsgModel('simple_grammar', log_math, 1.0, 10)
        fsg_model.add_silence('<sil>', 1, 0.5)
        word_id = fsg_model.word_id('<sil>')
        self.assertGreaterEqual(word_id, 0)
