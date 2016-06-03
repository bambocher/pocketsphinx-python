import os
import unittest

import sphinxbase.sphinxbase as sb
import pocketsphinx.pocketsphinx as ps


class Decoder(object):

    def __init__(self, hmm_path=None, lm_path=None, dict_path=None, lm_load=True,
                 logfn='/dev/null', keyphrase=None, kws_threshold=None, mmap=None):
        self.hmm_path = hmm_path
        self.lm_path = lm_path
        self.dict_path = dict_path
        self.model_path = 'pocketsphinx/model'
        self.data_path = 'pocketsphinx/test/data'
        self.goforward_raw = os.path.join(self.data_path, 'goforward.raw')
        self.goforward_mfc = os.path.join(self.data_path, 'goforward.mfc')
        self.hypothesis = None
        self.config = ps.Decoder.default_config()
        self.config.set_string('-hmm', self.hmm_path or os.path.join(self.model_path, 'en-us/en-us'))
        self.config.set_string('-lm', self.lm_path or os.path.join(self.model_path, 'en-us/en-us.lm.bin')) if lm_load else None
        self.config.set_string('-dict', self.dict_path or os.path.join(self.model_path, 'en-us/cmudict-en-us.dict'))
        self.config.set_string('-logfn', logfn)
        self.config.set_string('-keyphrase', keyphrase) if keyphrase else None
        self.config.set_float('-kws_threshold', kws_threshold) if kws_threshold else None
        self.config.set_boolean('-mmap', mmap) if mmap else None
        self.decoder = ps.Decoder(self.config)

    def get_hypothesis(self):
        return self.hypothesis

    def lookup_word(self, word):
        return self.decoder.lookup_word(word)

    def get_confidence(self, hypothesis):
        logmath = self.decoder.get_logmath()
        return logmath.exp(hypothesis.prob)

    def get_hypothesis_segments(self):
        return [seg.word for seg in self.decoder.seg()]

    def get_best_decodings(self, count):
        decodings = []
        for decoding, i in zip(self.decoder.nbest(), range(count)):
            decodings.append((decoding.hypstr, decoding.score))
        return decodings

    def run(self):
        self.decoder.start_utt()
        stream = open(self.goforward_raw, 'rb')
        while True:
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
        self.decoder.end_utt()
        stream.close()
        self.hypothesis = self.decoder.hyp()

    def run_cep(self):
        stream = open(self.goforward_mfc, 'rb')
        stream.read(4)
        buf = stream.read(13780)
        self.decoder.start_utt()
        self.decoder.process_cep(buf, False, True)
        self.decoder.end_utt()
        stream.close()
        self.hypothesis = self.decoder.hyp()


class TestDecoder(unittest.TestCase):

    def test_decoder_lookup_word(self):
        decoder = Decoder()
        word = decoder.lookup_word('hello')
        self.assertEqual(word, 'HH AH L OW')
        word = decoder.lookup_word('abcdf')
        self.assertEqual(word, None)

    def test_decoder_raw(self):
        decoder = Decoder()
        decoder.run()
        hypothesis = decoder.get_hypothesis()
        self.assertEqual(hypothesis.hypstr, 'go forward ten meters')
        self.assertEqual(hypothesis.best_score, -7066)
        confidence = decoder.get_confidence(hypothesis)
        self.assertEqual(confidence, 0.04042641466841839)

    def test_decoder_cep(self):
        decoder = Decoder()
        decoder.run_cep()
        hypothesis = decoder.get_hypothesis()
        self.assertEqual(hypothesis.hypstr, 'go forward ten meters')
        self.assertEqual(hypothesis.best_score, -7095)
        self.assertEqual(hypothesis.prob, -32715)

    def test_decoder_hypothesis_segments(self):
        decoder = Decoder()
        decoder.run()
        segments = decoder.get_hypothesis_segments()
        self.assertEqual(segments, ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>'])

    def test_decoder_best_decodings(self):
        decoder = Decoder()
        decoder.run()
        best_decodings = decoder.get_best_decodings(10)
        self.assertEqual(best_decodings, [
            ('go forward ten meters', -28034),
            ('go for word ten meters', -28570),
            ('go forward and majors', -28670),
            ('go forward and meters', -28681),
            ('go forward and readers', -28685),
            ('go forward ten readers', -28688),
            ('go forward ten leaders', -28695),
            ('go forward can meters', -28695),
            ('go forward and leaders', -28706),
            ('go for work ten meters', -28722)
        ])
