# -*- coding:utf8 -*-
from multiprocessing import Process
from time import sleep

from .IComponent import *

class CLOCK(IComponent):
    """CLOCK, DEAR TICKING CLOCK"""

    def __init__(self, bus, tick_interval=5):
        super().__init__(bus)

        self.setTickInterval(tick_interval)
        self.stop()

        self.KILL = False
        self.PROCESS = None

    def setTickInterval(self, tick_interval):
        self.TICK_INTERVAL = tick_interval

    def tick(self):
        self.bus.clock()

    def mainloop(self):
        while not self.KILL:
            if self.TICKING:
                self.tick()
            sleep(self.TICK_INTERVAL / 1000)
        self.KILL = False
        self.PROCESS = None

    def run(self):
        if self.PROCESS is None:
            self.PROCESS = Process(target=self.mainloop)
            self.PROCESS.start()
        return self.PROCESS

    def start(self):
        self.TICKING = True
        self.run()

    def stop(self):
        self.TICKING = False

    def kill(self):
        self.KILL = True

    def isRunning(self):
        return self.PROCESS is not None
