# -*- coding:utf8 -*-
from .components import *

class VirtualMachine(object):
    def __init__(self):
        self.bus = bus = BUS()

        self.clock = CLOCK(bus)
        self.cpu = CPU(bus)
        self.rom = ROM(bus).rangemap(0, 16635)
        self.ram = RAM(bus).rangemap(32768, 65535)
        self.io = IO(bus).rangemap(16636, 32767)

    def loadProgram(self, binary):
        self.rom.load(binary)

    def run(self):
        self.clock.run()
        self.clock.start()
