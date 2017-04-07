# -*- coding:utf8 -*-
from .MAPPED import *

class ROM(MAPPED):
    """READ ONLY MEMORY"""

    def write(*args):
        return

    def load(self, binary):
        size = len(binary)
        if size > self.getSize():
            raise ValueError('binary length is too big')
        for pos in range(size):
            self.map[pos] = binary[pos]

    def override(self, *args):
        """This function gives access to 'write'"""
        super().write(*args)
