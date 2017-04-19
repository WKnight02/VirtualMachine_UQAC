import unittest

from ...modules.logic.Operation import *

class OperationTestCase(unittest.TestCase):

    SOURCE_OK = {
        'SET A 0x1234': '1281 4660',
        'ADD B C': '4354 3',
		'JMP 0x1234': '256 4660',
		'EZ A': '13825',
		'HLT': '3840',
		'NOP': '0',
		'XOR D A': '8964 1',
        'DTA 64':'64',
        'DTA "Salut toi"': '83 97 108 117 116 32 116 111 105',
		'ST A B':'1809 2',
		'ST A 1':'1793 1',
        }

    SOURCE_NOT_OK = [
		'JMP A',
        'DTA "salut" 64',
        'ADD 0x1234 0x4567',
        'SET 0x1234 A',
        'SET B B',
		'EZ Z',
		'EZ 12',
		'NOP sjkqfvseqvfuqie<uhghZAYQdob hs qfeqg uskhfg uv ue<gv jefg wjfb x',
		'NOP A',

        ]

    def test_compile_ok(self):
        for ok, expected in self.SOURCE_OK.items():
            data = Operation.compile(ok)
            self.assertEqual(expected, data)

    def test_compile_not_ok(self):
        for bad in self.SOURCE_NOT_OK:
            try:
                data = Operation.compile(bad)
            except:
                self.assertTrue(True)
                continue

            # If we did not catch an exception
            self.assertEqual(data, None, bad)
