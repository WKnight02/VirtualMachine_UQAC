import unittest

from ...modules.logic.Operation import *

class OperationTestCase(unittest.TestCase):

    SOURCE_OK = {
        'SET A 0x1234': bytes((0x05, 0x01, 0x12, 0x34)),
        'ADD B C': bytes((0x11, 0x02, 0x00, 0x03)),
		'JMP 0x1234': bytes((0x01, 0x00, 0x12, 0x34)),
		'EZ A':bytes((0x36,0x01)),
		'HLT':bytes((0x0F,0x00)),
		'NOP':bytes((0x00,0x00)),
		'XOR D A':bytes((0x23,0x04,0x00,0x01))
        }

    SOURCE_NOT_OK = [
		'JMP A',
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