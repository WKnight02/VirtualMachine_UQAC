# -*- coding:utf8 -*-
import tkinter as tk

from . import Compiler
from .components import *
from .interfaces import ControllerInterface

__all__ = ['VirtualMachine']

class VirtualMachine(object):
    def __init__(self):
        self.bus = bus = BUS()

        self.clock = CLOCK(bus)
        self.cpu = CPU(bus)
        self.rom = ROM(bus).rangemap(0, 16635)
        self.ram = RAM(bus).rangemap(32768, 65535)
        self.term = TERM(bus).rangemap(16636, 32767)

    def createUI(self):
        self.window = root = tk.Tk()
        termUI = self.term.createUI(root)
        termUI.pack()

    def loadProgram(self, integers):
        self.rom.load(integers)

    def loadPseudoCompiledProgram(self, programLines):
        """This directly maps each value into the ROM"""
        self.loadProgram(Compiler.ParseTextProgramAsInt(programLines))

    def run(self):
        """Starts the clock event thread and starts the cycles"""
        print("Started the Clock's Thread...")
        self.clock.run()
        self.clock.start()
