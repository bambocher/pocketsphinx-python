import unittest

from .test_decoder import Decoder


class Continuous(Decoder):

    def __init__(self, *args, **kwargs):
        super(Continuous, self).__init__(*args, **kwargs)

    def run(self):
        in_speech = False
        stream = open(self.goforward_raw, 'rb')
        self.decoder.start_utt()
        while True:
            buf = stream.read(1024)
            if buf:
                self.decoder.process_raw(buf, False, False)
                if self.decoder.get_in_speech() != in_speech:
                    in_speech = self.decoder.get_in_speech()
                    if not in_speech:
                        self.decoder.end_utt()
                        self.hypothesis = self.decoder.hyp()
                        self.decoder.start_utt()
            else:
                break
        self.decoder.end_utt()
        stream.close()


class TestContinuous(unittest.TestCase):

    def test_continuous(self):
        continuous = Continuous()
        continuous.run()
        hypothesis = continuous.get_hypothesis()
        self.assertEqual(hypothesis.hypstr, 'go forward ten meters')
