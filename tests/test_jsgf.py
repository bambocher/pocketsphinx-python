import os
import unittest

import sphinxbase.sphinxbase as sb

from .test_decoder import Decoder


class Jsgf(Decoder):

    def __init__(self, *args, **kwargs):
        super(Jsgf, self).__init__(*args, **kwargs)

    def switch_to_jsgf_grammar(self):
        jsgf = sb.Jsgf(os.path.join(self.data_path, 'goforward.gram'))
        rule = jsgf.get_rule('goforward.move2')
        fsg = jsgf.build_fsg(rule, self.decoder.get_logmath(), 7.5)
        fsg.writefile('goforward.fsg')

        self.decoder.set_fsg('goforward', fsg)
        self.decoder.set_search('goforward')


class TestJsgf(unittest.TestCase):

    def test_jsgf(self):
        hmm_path = os.path.join('pocketsphinx/model', 'en-us/en-us')
        lm_path = os.path.join('pocketsphinx/test/data', 'turtle.lm.bin')
        dict_path = os.path.join('pocketsphinx/test/data', 'turtle.dic')

        jsgf = Jsgf(hmm_path, lm_path, dict_path)
        jsgf.run()
        hypothesis = jsgf.get_hypothesis()
        # Decoding with 'turtle' language model
        self.assertEqual(hypothesis.hypstr, 'go forward ten meters')

        # Switch to JSGF grammar
        jsgf.switch_to_jsgf_grammar()
        jsgf.run()
        hypothesis = jsgf.get_hypothesis()
        # Decoding with 'goforward' grammar
        self.assertEqual(hypothesis.hypstr, 'go forward ten meters')
