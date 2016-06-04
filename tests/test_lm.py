import os
import unittest

import sphinxbase as sb

from .test_decoder import Decoder


class Lm(Decoder):

    def __init__(self, *args, **kwargs):
        super(Lm, self).__init__(*args, **kwargs)

    def load_turtle_lm(self):
        lm = sb.NGramModel(self.config, self.decoder.get_logmath(),
                           os.path.join('deps/pocketsphinx/test/data', 'turtle.lm.bin'))

        # TODO: TypeError: in method 'NGramModel_prob', argument 3 of type 'char const *const *'
#        print(lm.prob(1, ['you']))
#        print(lm.prob(2, ['are', 'you']))
#        print(lm.prob(3, ['you', 'are', 'what']))
#        print(lm.prob(3, ['lost', 'are', 'you']))

        self.decoder.set_lm('turtle', lm)
        self.decoder.set_search('turtle')

    def add_word(self, word, phones, update):
        self.decoder.add_word(word, phones, update)


class TestLm(unittest.TestCase):

    def test_lm(self):
        hmm_path = os.path.join('deps/pocketsphinx/model', 'en-us/en-us')
        lm_path = os.path.join('deps/pocketsphinx/model', 'en-us/en-us.lm.bin')
        dict_path = os.path.join('deps/pocketsphinx/test/data', 'defective.dic')

        # Create a decoder with 'defective' language model
        lm = Lm(hmm_path, lm_path, dict_path, mmap=False)
        lm.run()
        hypothesis = lm.get_hypothesis()
        # Decoding with 'defective' language model
        self.assertEqual(hypothesis.hypstr, '')

        # Load 'turtle' language model and decode again
        lm.load_turtle_lm()
        lm.run()
        hypothesis = lm.get_hypothesis()
        # Decoding with 'turtle' language model
        self.assertEqual(hypothesis.hypstr, '')

        # The word 'meters' isn't in the loaded dictionary.
        # Let's add it manually.
        lm.add_word('foobie', 'F UW B IY', False)
        lm.add_word('meters', 'M IY T ER Z', True)
        lm.run()
        hypothesis = lm.get_hypothesis()
        # Decoding with 'turtle' language model
        self.assertEqual(hypothesis.hypstr, 'foobie meters meters')
