"""
The editor's interface
"""
import tkinter as tk
from tkinter import filedialog

__all__ = ['TermInterface']

class TermInterface(tk.Frame):
    """Terminal's interface
    """

    def __init__(self, root, height, width, *args, **kargs):
        """PUTE"""
        super().__init__(root, *args, **kargs)
        self.height = height
        self.width = width

        self.term = tk.Text(self,
            height=height, width=width,
            bg='black', fg='white',
            highlightbackground='grey',
            highlightcolor='white'
            )
        self.term.insert(tk.END, ' ' * width * height)
        self.disable()

        self.term.pack()

    def enable(self):
        self.term.config(state=tk.NORMAL)
        return self.term

    def disable(self):
        self.term.config(state=tk.DISABLED)
        return self.term

    def setCharAt(self, position, char):
        term = self.enable()
        term.delete(
            '1.%d' % position,
            '1.%d' % (position+1)
            )
        term.insert('1.%d' % position, char[0])

        # Clear any extra char + close edition
        term.delete('1.%d' % (self.height * self.width), tk.END)
        self.disable()

if __name__ == '__main__':

    window = tk.Tk()
    io = TermInterface(window, height=25, width=80)
    io.pack()

    io.setCharAt(char='X', position=io.width * 2 + 3)
    io.setCharAt(char='O', position=io.height * io.width - 1)
    io.setCharAt(char='N', position=io.height * io.width + 1)

    window.mainloop()
