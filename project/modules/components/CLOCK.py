# -*- coding:utf8 -*-
from multiprocessing import Process
from threading import Thread
from time import sleep

from .IComponent import *

class CLOCK(IComponent):
    """CLOCK, DEAR TICKING CLOCK"""

    def __init__(self, bus, tick_interval=5):
        super().__init__(bus)

        self.setTickInterval(tick_interval)
        self.stop()

        self.KILL = False
        self.THREAD = None

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
        self.THREAD = None

    def run(self):
        if self.THREAD is None:
            self.THREAD = Thread(target=self.mainloop)
            self.THREAD.start()
        return self.THREAD

    def start(self):
        self.TICKING = True
        self.run()

    def stop(self):
        self.TICKING = False

    def kill(self):
        self.KILL = True

    def isRunning(self):
        return self.THREAD is not None
