"""
The editor's interface
"""
import tkinter as tk
from tkinter import filedialog

__all__ = ['IOInterface']

class IOInterface(tk.Tk):
    """IO's interface
    """

    def __init__(self, *args, **kargs):
        """PUTE"""
        super().__init__()
        self.resizable(width=False, height=False)

        self.term = tk.Text(self,
            height=25, width=80,
            bg='black', fg='white',
            highlightbackground='grey',
            highlightcolor='white'
            )
        self.term.pack()

if __name__ == '__main__':
    io = IOInterface()
    io.mainloop()
