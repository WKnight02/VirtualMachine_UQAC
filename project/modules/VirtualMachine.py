# -*- coding:utf8 -*-
import tkinter as tk
import time

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

        VM.warmup()
        ui = VM.createUI()
        ui.mainloop()

    def __init__(self):
        self.bus = bus = BUS()

        self.clock = CLOCK(bus)
        self.cpu = CPU(bus)
        self.rom = ROM(bus).rangemap(0, 16635)
        self.ram = RAM(bus).rangemap(32768, 65535)
        self.term = TERM(bus).sizemap(16896, 2000)
        self.keyboard = KEYBOARD(bus).sizemap(16636, 1)

    def createUI(self):
        self.window = root = tk.Tk()
        root.resizable(height=False, width=False)

        # Setting up the terminal
        def onClose(*args):
            self.clock.kill()
            root.destroy()
        root.protocol('WM_DELETE_WINDOW', onClose)
        root.bind('<Escape>', onClose)

        # Setting up the keyboard register
        root.bind('<Key>', self.keyboard.onPress)

        # Packing the terminal
        termUI = self.term.createUI(root)
        termUI.pack(fill=tk.BOTH)

        # Packing the controller
        controllerUI = ControllerInterface(root)
        controllerUI.setControlledClock(self.clock)
        controllerUI.setControlledCpu(self.cpu)
        controllerUI.pack(fill=tk.BOTH)
        controllerUI.refresh()

        # Assigning the refresh method to the UI/CLOCK
        def tickCallback(): # Could crash on window closing...
            try: controllerUI.refresh()
            except: pass
        self.clock.setTickCallback(tickCallback)

        return root

    def loadProgram(self, integers):
        self.rom.load(integers)

    def loadPseudoCompiledProgram(self, programLines):
        """This directly maps each value into the ROM"""
        self.loadProgram(Compiler.ParseTextProgramAsInt(programLines))

    def warmup(self):
        """This starts the CLOCK's Thread, but doesn't start the clock"""
        self.clock.run()

    def run(self):
        """Starts the clock event thread and starts the cycles"""
        self.warmup()
        self.clock.start()

    def stop(self):
        """Stops the clock's mainloop"""
        self.clock.stop()

    def kill(self):
        """Kills the clock's mainloop thread (cleaner)"""
        self.clock.kill()
