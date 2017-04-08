# -*- coding:utf8 -*-
from .MAPPED import *

class ROM(MAPPED):
    """READ ONLY MEMORY"""

    def write(*args):
        return

    def load(self, binary):

        selfSize = self.getSize()

        try:
            size = len(binary)
            if size > selfSize:
                raise ValueError('Data length is too big [%d > %d]' % (size, selfSize))
        except:
            pass

        pos = 0
        for data in binary:
            if pos >= selfSize:
                raise OutOfMemoryException('ROM ran out of memory while loading data [%d]' % selfSize)
            self.map[pos] = data
            pos += 1

    def override(self, *args):
        """This function gives access to 'write'"""
        super().write(*args)
