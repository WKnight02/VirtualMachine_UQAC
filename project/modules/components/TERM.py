# -*- coding:utf8 -*-
from .MAPPED import *

from ..interfaces.TermInterface import *

class TERM(MAPPED):
    """INPUT / OUTPUT"""

    def read(*args):
        return

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.ui = None

    def createUI(self, root, height=25, width=80, *args, **kargs):
        self.ui = TermInterface(root, height, width, *args, **kargs)
        return self.ui

    def write(self, position, value):
        if self.ui is not None:
            try:
                char = chr(value)
            except:
                char = '?'

            self.ui.setCharAt(position, char)
