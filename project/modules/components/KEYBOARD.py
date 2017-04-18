# -*- coding:utf8 -*-
from .MAPPED import *

class KEYBOARD(MAPPED):
    """READ KEYBOARD"""

    """Debug
    def read(self, *args):
        data = super().read(*args)
        print(*args, data)
        return data
    """

    def onPress(self, event):
        """Pass some event and tries to register it to memory"""
        try:
            code = ord(event.char)
        except:
            code = ord('?')
        super().write(0, code)
