import unittest

from ...modules.logic.Operation import *

class OperationTestCase(unittest.TestCase):

    SOURCE_OK = {
        'SET A 0x4521': bytes((0x05, 0x01, 0x12, 0x34)),
        'ADD B C': bytes((0x11, 0x02, 0x00, 0x03)),
        }

    SOURCE_NOT_OK = [
        'ADD 0x1234 0x4567',
        'SET 0x1234 A',
        'SET B B',
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
            self.assertEqual(data, None)
