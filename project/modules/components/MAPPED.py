# -*- coding:utf8 -*-
from .IComponent import *

class MAPPED(IComponent):
    """COMPONENT SELF AWARE OF SOME MAPPING"""

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.start = 0
        self.end = 0
        self.map = []

    def rangemap(self, start, end):
        self.start = start
        self.end = end
        self.clear()
        return self

    def sizemap(self, start, size):
        return self.rangemap(start, start+size)

    def clear(self):
        self.map = [0 for i in range(self.start, self.end + 1)]
        return self

    def getSize(self):
        size = self.end - self.start
        return size if size > 0 else None

    def read(self, position):
        return self.map[position]

    def write(self, position, value):
        self.map[position] = value
        return self

    def event(self):
        addr = self.bus.ADDR
        if addr in range(self.start, self.end + 1):

            # do not forget the offset
            relative = addr - self.start

            if self.bus.reading():
                self.bus.DATA = self.read(relative)
            elif self.bus.writing():
                self.write(relative, self.bus.DATA)
