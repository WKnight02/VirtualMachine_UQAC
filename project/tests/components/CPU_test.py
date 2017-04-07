import unittest

from ...modules.components.BUS import *
from ...modules.components.CPU import *
from ...modules.components.ROM import *
from ...modules.components.RAM import *

class CPUTestCase(unittest.TestCase):

    def setUp(self):
        bus = self.bus = BUS()
        self.cpu = CPU(bus)
        self.rom = ROM(bus).rangemap(0, (1<<16) -1)
        self.ram = RAM(bus).rangemap(1<<16, (1<<16) * 2 - 1)

    def test_cpu_operation_on_register(self):
        cpu = self.cpu

        a = 0xFFFF
        b = 0x0001

        cpu.setRegister(4, a)
        cpu.setRegister(2, b)
        cpu.invoke('SUB')(4, 2)

        reg4 = cpu.getRegister(4)
        self.assertEqual(reg4, a - b, reg4)
        self.assertEqual(cpu.getStateBit(CPU.STATE_CARRY), 0)

        cpu.setRegister(1, a)
        cpu.invoke('ADD')(1, 2)

        reg1 = cpu.getRegister(1)
        self.assertEqual(reg1, 0, reg1)
        self.assertEqual(cpu.getStateBit(CPU.STATE_CARRY), 1)

    def test_cpu_cycle(self):

        # SET A 0xFFFE
        # SET B 0x0001
        # ADD A B
        program = [
            0x0501, 0xFFFE,
            0x0502, 0x0001,
            0x1101, 0x0002
        ]

        self.rom.load(program)
        cpu = self.cpu

        self.assertEqual(0x0000, cpu.getRegister(1))

        cpu.clock()
        self.assertEqual(2, cpu.PC)
        self.assertEqual(0xFFFE, cpu.getRegister(1))
        self.assertEqual(0x0000, cpu.getRegister(2))

        cpu.clock()
        self.assertEqual(4, cpu.PC)
        self.assertEqual(0xFFFE, cpu.getRegister(1))
        self.assertEqual(0x0001, cpu.getRegister(2))

        cpu.clock()
        self.assertEqual(6, cpu.PC)
        self.assertEqual(0xFFFF, cpu.getRegister(1))
        self.assertEqual(0x0001, cpu.getRegister(2))
