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


class TestPhoneme(TestCase):

    def __init__(self, *args, **kwargs):
        self.ps = Pocketsphinx(
            lm=False,
            dic=False,
            allphone='deps/pocketsphinx/model/en-us/en-us-phone.lm.bin',
            lw=2.0,
            pip=0.3,
            beam=1e-200,
            pbeam=1e-20,
            mmap=False
        )
        self.ps.decode()
        super(TestPhoneme, self).__init__(*args, **kwargs)

    def test_phoneme_hypothesis(self):
        self.assertEqual(
            self.ps.hypothesis(),
            'SIL G OW F AO R D T AE N NG IY ZH ER S SIL'
        )

    def test_phoneme_best_phonemes(self):
        self.assertEqual(self.ps.segments(), [
            'SIL',
            'G',
            'OW',
            'F',
            'AO',
            'R',
            'D',
            'T',
            'AE',
            'N',
            'NG',
            'IY',
            'ZH',
            'ER',
            'S',
            'SIL'
        ])
