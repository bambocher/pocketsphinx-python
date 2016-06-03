import unittest

from .test_decoder import Decoder


class Kws(Decoder):

    def __init__(self, *args, **kwargs):
        super(Kws, self).__init__(*args, **kwargs)

    def run(self):
        keyword = None
        stream = open(self.goforward_raw, 'rb')
        self.decoder.start_utt()
        while True:
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
            else:
                break
            if self.decoder.hyp():
                # Detected keyword, perform action and restart search
                keyword = [(seg.word, seg.prob, seg.start_frame, seg.end_frame) for seg in self.decoder.seg()]
                self.decoder.end_utt()
                self.decoder.start_utt()
        self.decoder.end_utt()
        stream.close()
        return keyword


class TestKws(unittest.TestCase):

    def test_kws(self):
        kws = Kws(lm_load=False, keyphrase='forward', kws_threshold=1e+20)
        keyword = kws.run()
        self.assertEqual(keyword, [('forward', 883, 63, 121)])
