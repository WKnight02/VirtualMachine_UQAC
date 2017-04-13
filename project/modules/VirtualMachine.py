# -*- coding:utf8 -*-
import tkinter as tk

from . import Compiler
from .components import *
from .interfaces import ControllerInterface

__all__ = ['VirtualMachine']

class VirtualMachine(object):

    @classmethod
    def SpawnAndExecute(cls, file):
        VM = cls()

        with open(file, 'r') as f:
            VM.loadPseudoCompiledProgram(f)
        ui = VM.createUI()

        VM.run()
        ui.mainloop()

    def __init__(self):
        self.bus = bus = BUS()

        self.clock = CLOCK(bus)
        self.cpu = CPU(bus)
        self.rom = ROM(bus).rangemap(0, 16635)
        self.ram = RAM(bus).rangemap(32768, 65535)
        self.term = TERM(bus).sizemap(16636, 2000)

    def createUI(self):
        self.window = root = tk.Tk()

        def onClose(*args):
            self.clock.kill()
            root.destroy()
        root.protocol('WM_DELETE_WINDOW', onClose)
        root.bind('<Escape>', onClose)

        termUI = self.term.createUI(root)
        termUI.pack()

        return root

    def loadProgram(self, integers):
        self.rom.load(integers)

    def loadPseudoCompiledProgram(self, programLines):
        """This directly maps each value into the ROM"""
        self.loadProgram(Compiler.ParseTextProgramAsInt(programLines))

    def run(self):
        """Starts the clock event thread and starts the cycles"""
        self.clock.run()
        self.clock.start()

    def stop(self):
        """Stops the clock's mainloop"""
        self.clock.stop()

    def kill(self):
        """Kills the clock's mainloop thread (cleaner)"""
        self.clock.kill()
