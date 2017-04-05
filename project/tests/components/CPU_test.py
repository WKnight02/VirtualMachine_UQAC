import unittest

from ...modules.components.BUS import *
from ...modules.components.CPU import *
from ...modules.components.RAM import *

class CPUTestCase(unittest.TestCase):

    def setUp(self):
        bus = self.bus = BUS()
        self.cpu = CPU(bus)
        self.ram = RAM(bus).rangemap(0, 1<<16)

    def test_cpu_operation(self):
        pass
