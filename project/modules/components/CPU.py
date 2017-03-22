# -*- coding:utf8 -*-
from .IComponent import *
from .ALU import *

class CPU(IComponent):
    """CENTRAL PROCESSING UNIT"""

    def __init__(self, bus):
        super().__init__(bus)
        self.ALU = ALU()

    def fetch(self):
        pass

    def decode(self):
        pass

    def execute(self):
        pass

    def clock(self):
        self.fetch()
        self.decode()
        self.execute()
