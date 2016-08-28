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
from pocketsphinx import Pocketsphinx, NGramModel


class TestLm(TestCase):

    def test_lm(self):
        ps = Pocketsphinx(
            dic='deps/pocketsphinx/test/data/defective.dic',
            mmap=False
        )

        # Decoding with 'defective' dictionary
        ps.decode()
        self.assertEqual(ps.hypothesis(), '')

        # Switch to 'turtle' language model
        turtle_lm = 'deps/pocketsphinx/test/data/turtle.lm.bin'
        lm = NGramModel(ps.get_config(), ps.get_logmath(), turtle_lm)
        ps.set_lm('turtle', lm)
        ps.set_search('turtle')

        # Decoding with 'turtle' language model
        ps.decode()
        self.assertEqual(ps.hypothesis(), '')

        # The word 'meters' isn't in the loaded dictionary
        # Let's add it manually
        ps.add_word('foobie', 'F UW B IY', False)
        ps.add_word('meters', 'M IY T ER Z', True)

        # Decoding with 'turtle' language model
        ps.decode()
        self.assertEqual(ps.hypothesis(), 'foobie meters meters')
