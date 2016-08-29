#!/usr/bin/env python
from __future__ import print_function
from pocketsphinx import Pocketsphinx

ps = Pocketsphinx()
ps.decode()

print('Hypothesis:', ps.hypothesis())
print('Probability:', ps.probability())
print('Score:', ps.score())
print('Segments:', ps.segments())
print('Confidence:', ps.confidence())
print('Best:', *ps.best(), sep='\n')
