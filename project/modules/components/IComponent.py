# -*- coding:utf8 -*-

class IComponent(object):
    """Component interface"""

    def __init__(self, bus=None):
        if bus is not None: bus.register(self)
        self.bus = bus

    def clock(self): pass
    def event(self): pass
