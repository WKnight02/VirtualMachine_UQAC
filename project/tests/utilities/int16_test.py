import unittest

from ...modules.utilities import int16

class int16TestCase(unittest.TestCase):

    def test_overflow(self):

        # inputs / outputs
        io = {
            int16.MAX:      (True, 0),
            int16.MAX + 1:  (True, 1),
            int16.MAX - 1:  (False, int16.MAX - 1),
            }

        for n, expected in io.items():
            self.assertEqual(int16.Overflow(n), expected)

    def test_bit_access(self):

        # Test number
        n = 0b10010011

        # Binary representation of test number
        # bn[0] = least bit
        bn = [1, 1, 0, 0, 1, 0, 0, 1]

        for i in range(len(bn)):
            self.assertEqual(int16.BitGet(n, i), bn[i], i)

        # Expected modified results after bit setting
        for i in range(len(n)):
            for v in (0, 1):
                self.assertEqual(
                    int16.BitGet(int16.BitSet(i, v), i),
                    v,
                    (i, v)
                )
