# -*- coding:utf8 -*-

class IComponent(object):
    """Component interface"""

    def __init__(self, bus=None):
        if bus: bus.register(self)
        self.bus = bus

    def clock(): pass
    def event(): pass
