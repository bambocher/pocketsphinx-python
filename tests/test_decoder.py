# Copyright (c) 1999-2016 Carnegie Mellon University. All rights
# reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# This work was supported in part by funding from the Defense Advanced
# Research Projects Agency and the National Science Foundation of the
# United States of America, and the CMU Sphinx Speech Consortium.
#
# THIS SOFTWARE IS PROVIDED BY CARNEGIE MELLON UNIVERSITY ``AS IS'' AND
# ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL CARNEGIE MELLON UNIVERSITY
# NOR ITS EMPLOYEES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from unittest import TestCase
from pocketsphinx import Pocketsphinx


class TestRawDecoder(TestCase):

    def __init__(self, *args, **kwargs):
        self.ps = Pocketsphinx()
        self.ps.decode()
        super(TestRawDecoder, self).__init__(*args, **kwargs)

    def test_raw_decoder_lookup_word(self):
        self.assertEqual(self.ps.lookup_word('hello'), 'HH AH L OW')
        self.assertEqual(self.ps.lookup_word('abcdf'), None)

    def test_raw_decoder_hypothesis(self):
        self.assertEqual(self.ps.hypothesis(), 'go forward ten meters')
        self.assertEqual(self.ps.score(), -7066)
        self.assertEqual(self.ps.confidence(), 0.04042641466841839)

    def test_raw_decoder_segments(self):
        self.assertEqual(self.ps.segments(), [
            '<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>'
        ])

    def test_raw_decoder_best_hypothesis(self):
        self.assertEqual(self.ps.best(), [
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


class TestCepDecoder(TestCase):

    def test_cep_decoder_hypothesis(self):
        ps = Pocketsphinx()
        with open('deps/pocketsphinx/test/data/goforward.mfc', 'rb') as f:
            with ps.start_utterance():
                f.read(4)
                buf = f.read(13780)
                ps.process_cep(buf, False, True)
        self.assertEqual(ps.hypothesis(), 'go forward ten meters')
        self.assertEqual(ps.score(), -7095)
        self.assertEqual(ps.probability(), -32715)
