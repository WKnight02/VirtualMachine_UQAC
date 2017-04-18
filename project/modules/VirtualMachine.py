# -*- coding:utf8 -*-
import tkinter as tk
import os.path
import time

from . import Compiler
from .components import *
from .interfaces import ControllerInterface

__all__ = ['VirtualMachine']

class VirtualMachine(object):

    UnknownProgramName = 'Unknown Program'

    @classmethod
    def SpawnAndExecute(cls, file):
        """Utility method: Just give a valid .tpc filename, and it will
        hand you a Virtual Machine ready to run.
        """

        VM = cls()

        with open(file, 'r') as f:
            VM.loadPseudoCompiledProgram(f, name=os.path.basename(file))

        VM.warmup()
        ui = VM.createUI()
        ui.mainloop()

    def __init__(self, name='Virtual Machine'):
        self.bus = bus = BUS()

        self.clock = CLOCK(bus)
        self.cpu = CPU(bus)
        self.rom = ROM(bus).rangemap(0, 16635)
        self.ram = RAM(bus).rangemap(32768, 65535)
        self.term = TERM(bus).sizemap(16896, 2000)
        self.keyboard = KEYBOARD(bus).sizemap(16636, 1)

        self.setName(name)
        self.setProgramName('Unknown Program')

    def setName(self, name):
        self.name = name
        return self

    def getName(self, name):
        self.name = name

    def setProgramName(self, name):
        self.programName = name
        return self

    def getProgramName(self):
        return self.programName

    def getWindowTitle(self):
        return self.name + ' - ' + self.programName

    def createUI(self, **kargs):
        """Give it a name with 'name=...'"""
        self.window = root = tk.Tk()
        root.resizable(height=False, width=False)

        # Set the Virtual Machine UI's title
        root.title(kargs.get('title', self.getWindowTitle()))

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
        controllerUI.setControlledVM(self)
        controllerUI.pack(fill=tk.BOTH)
        controllerUI.refresh()

        # Assigning the refresh method to the UI/CLOCK
        def tickCallback(): # Could crash on window closing...
            try: controllerUI.refresh()
            except: pass
        self.clock.setTickCallback(tickCallback)

        return root

    def loadProgram(self, integers, **kargs):
        """Load program from (integer list)-like and sets the name of the
        loaded program (for the UI to display)"""
        self.rom.load(integers)
        self.setProgramName(kargs.get('name', self.UnknownProgramName))

    def loadPseudoCompiledProgram(self, programLines, **kargs):
        """This load a program from (String lines) list representing
        integers separated by ' '(spaces)."""
        self.loadProgram(Compiler.ParseTextProgramAsInt(programLines), **kargs)

    def warmup(self):
        """This starts the CLOCK's Thread, but doesn't start the clock"""
        self.clock.run()

    def run(self):
        """Starts everything, the VM will be running right on"""
        self.warmup()
        self.clock.start()

    def stop(self):
        """Stops the clock's mainloop, only disallow ticking, doesn't kill it."""
        self.clock.stop()

    def kill(self):
        """Kills the clock's mainloop thread (cleaner)"""
        self.clock.kill()

    def restart(self):
        """Resets writable components, keeps ROM."""

        self.cpu.initRegisters()

        self.ram.clear()
        self.term.clear()
        self.keyboard.clear()

        self.warmup()
