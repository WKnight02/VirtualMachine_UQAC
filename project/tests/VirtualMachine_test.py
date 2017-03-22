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
