# -*- coding:utf8 -*-
from ..utilities import intB
from .IComponent import *

__all__ = ['BUS']

class BUS(IComponent):
    """BUS, FOR COMMUNICATION"""

    def __init__(self):
        self.REGISTERED_COMPONENT = set()
        self.reset()

    def reset(self):
        self.ADDR = 0
        self.DATA = 0
        self.waiting(True)

    def register(self, *components):
        for component in components:
            self.REGISTERED_COMPONENT.add(component)
        return self

    def clock(self):
        for component in self.REGISTERED_COMPONENT:
            component.clock()

    def event(self):
        # Say wut ?
        for component in self.REGISTERED_COMPONENT:
            component.event()

    def waiting(self, bool=False):
        if bool: self.MODE = 0
        return self.MODE == 0

    def reading(self, bool=False):
        if bool: self.MODE = 1
        return self.MODE == 1

    def writing(self, bool=False):
        if bool: self.MODE = 2
        return self.MODE == 2

    def read(self, addr):
        self.reading(True)
        self.ADDR = addr
        self.event()
        self.waiting(True)
        return self.DATA

    def write(self, addr, data):
        self.writing(True)
        self.ADDR = addr
        self.DATA = data
        self.event()
        self.waiting(True)
