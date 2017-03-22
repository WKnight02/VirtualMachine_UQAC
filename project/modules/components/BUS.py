# -*- coding:utf8 -*-
from ..utilities import intB
from .IComponent import *

__all__ = ['BUS']

class BUS(IComponent):
    """BUS, FOR COMMUNICATION"""

    def __init__(self):
        this.REGISTERED_COMPONENT = set()
        this.ADDR = None
        this.

    def register(self, component: IComponent):
        this.REGISTERED_COMPONENT.add(component)

    def clock():
        for component in this.REGISTERED_COMPONENT:
            component.clock()
