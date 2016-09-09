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
import os
import sys
from sphinxbase import *
from .pocketsphinx import *


DefaultConfig = Decoder.default_config


def get_model_path():
    """ Return path to the model. """
    return os.path.join(os.path.dirname(__file__), 'model')


def get_data_path():
    """ Return path to the model. """
    return os.path.join(os.path.dirname(__file__), 'data')


class Phrase(object):

    def __init__(self, phrase, probability, score):
        self.phrase = phrase
        self.probability = probability
        self.score = score

    def __str__(self):
        return self.phrase


class Pocketsphinx(Decoder):

    def __init__(self, **kwargs):
        model_path = get_model_path()
        data_path = get_data_path()

        self.goforward = os.path.join(data_path, 'goforward.raw')

        if kwargs.get('dic') is not None and kwargs.get('dict') is None:
            kwargs['dict'] = kwargs.pop('dic')

        if kwargs.get('hmm') is None:
            kwargs['hmm'] = os.path.join(model_path, 'en-us')

        if kwargs.get('lm') is None:
            kwargs['lm'] = os.path.join(model_path, 'en-us.lm.bin')

        if kwargs.get('dict') is None:
            kwargs['dict'] = os.path.join(model_path, 'cmudict-en-us.dict')

        if kwargs.pop('verbose', False) is False:
            if sys.platform.startswith('win'):
                kwargs['logfn'] = 'nul'
            else:
                kwargs['logfn'] = '/dev/null'

        config = DefaultConfig()

        for key, value in kwargs.items():
            if isinstance(value, bool):
                config.set_boolean('-{}'.format(key), value)
            elif isinstance(value, int):
                config.set_int('-{}'.format(key), value)
            elif isinstance(value, float):
                config.set_float('-{}'.format(key), value)
            elif isinstance(value, str):
                config.set_string('-{}'.format(key), value)

        super(Pocketsphinx, self).__init__(config)

    def decode(self, audio=None, max_samples=1024,
               no_search=False, full_utt=False, callback=None):
        keyphrase = self.get_config().get_string('-keyphrase')
        self.start_utt()
        with open(audio or self.goforward, 'rb') as f:
            while True:
                buf = f.read(max_samples)
                if buf:
                    self.process_raw(buf, no_search, full_utt)
                else:
                    break
                if keyphrase and self.hyp():
                    self.end_utt()
                    if callback:
                        callback(self)
                    self.start_utt()
        self.end_utt()

    def phrase(self):
        hyp = self.hyp()
        if hyp:
            return Phrase(hyp.hypstr, hyp.prob, hyp.best_score)

    def segments(self):
        return [s.word for s in self.seg()]

    def hypothesis(self):
        hyp = self.hyp()
        if hyp:
            return hyp.hypstr

    def probability(self):
        hyp = self.hyp()
        if hyp:
            return hyp.prob

    def score(self):
        hyp = self.hyp()
        if hyp:
            return hyp.best_score

    def best(self, count=10):
        return [
            (h.hypstr, h.score)
            for h, i in zip(self.nbest(), range(count))
        ]

    def confidence(self):
        hyp = self.hyp()
        if hyp:
            return self.get_logmath().exp(hyp.prob)


class Continuous(Pocketsphinx):

    def __init__(self, **kwargs):
        audio = kwargs.pop('audio', None)
        super(Continuous, self).__init__(**kwargs)
        self.stream = open(audio or self.goforward, 'rb')
        self.in_speech = False
        self.start_utt()

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            buf = self.stream.read(1024)
            if buf:
                self.process_raw(buf, False, False)
                if self.get_in_speech() != self.in_speech:
                    self.in_speech = self.get_in_speech()
                    if not self.in_speech:
                        self.end_utt()
                        phrase = self.phrase()
                        if phrase:
                            return phrase
                        self.start_utt()
                continue
            else:
                self.stream.close()
                raise StopIteration

    def next(self):
        self.__next__()
