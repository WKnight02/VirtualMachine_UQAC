# -*- coding:utf8 -*-
from .MAPPED import *

from ..interfaces.TermInterface import *

class TERM(MAPPED):
    """INPUT / OUTPUT"""

    def read(*args):
        """Deactivated"""
        return

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.ui = None

    def clear(self):
        super().clear()
        if self.ui is not None:
            self.ui.clearAll()

    def createUI(self, root, height=25, width=80, *args, **kargs):
        """Create the UI and return reference to it"""
        self.ui = TermInterface(root, height, width, *args, **kargs)
        return self.ui

    def write(self, position, value):
        """Write value as char into the Text (Tkinter UI) at some position.
        The internal buffer (self.map) is still used in order to avoid calls
        to self.ui.setCharAt(...) because its hell of messy (LAG)
        """
        if self.ui is not None:
            # AVOID ULTRA HARDCORE LAG
            if value == super().read(position): return

            try:
                char = chr(value)
            except:
                char = '?'

            # Could crash on window closing...
            super().write(position, value)
            try: self.ui.setCharAt(position, char)
            except: return

            """Footnote: The other way would have been to generate the full
            display from the buffer, as it would tend to not be corrupted,
            compared to the Tkinter element, which sometimes messes up...
            But this is still fine for now and tomorrow. Why not.
            Its working really well as far as it goes.
            Even if it slightly concerns me.
            Just believe.
            Do it.
            """
