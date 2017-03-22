import unittest

from ...modules.components.BUS import *
from ...modules.components.RAM import *

class BUSTestCase(unittest.TestCase):

    def setUp(self):
        self.bus = bus = BUS()
        self.ram = RAM(bus).rangemap(0, 64)

    def test_bus_write_to_ram(self):
        bus = self.bus
        ram = self.ram
        data = 123
        addr = 16

        self.assertEqual(0, ram.map.count(data))

        bus.ADDR = addr
        bus.DATA = data
        bus.writing(True)
        bus.event()

        self.assertEqual(1, ram.map.count(data))
        self.assertEqual(data, ram.read(addr))
        self.assertNotEqual(data, ram.read(0))

        bus.ADDR = 9999
        bus.DATA = data
        bus.writing(True)
        bus.event()

        self.assertEqual(1, ram.map.count(data))
