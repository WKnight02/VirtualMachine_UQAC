import unittest

from ..modules.VirtualMachine import *

class VirtualMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.vm = VirtualMachine()

    def test_loadProgram(self):
        data = b"ABCDEF"
        self.vm.loadProgram(data)
        for i in range(len(data)):
            self.assertEqual(data[i], self.vm.rom.read(i))

    def test_loadPseudoCompiledProgram(self):
        programLines = [
            '1 2 3 4',
            '9 8 7 6',
            '9999999',
        ]

        self.vm.loadPseudoCompiledProgram(programLines)

        i = 0
        for lines in programLines:
            for value in lines.split(' '):
                self.assertEqual(int(value), self.vm.rom.map[i])
                i += 1
