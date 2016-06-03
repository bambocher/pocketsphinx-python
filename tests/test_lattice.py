import unittest

from .test_decoder import Decoder


class Lattice(Decoder):

    def __init__(self, *args, **kwargs):
        super(Lattice, self).__init__(*args, **kwargs)

    def get_lattice(self):
        return self.decoder.get_lattice()


class TestLattice(unittest.TestCase):

    def test_lattice(self):
        lattice = Lattice()
        lattice.run()
        l = lattice.get_lattice()
        result = l.write('goforward.lat')
        self.assertEqual(result, None)
        l = lattice.get_lattice()
        result = l.write_htk('goforward.htk')
        self.assertEqual(result, None)
