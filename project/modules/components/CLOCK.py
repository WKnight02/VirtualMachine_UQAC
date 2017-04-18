# -*- coding:utf8 -*-
from multiprocessing import Process
from threading import Thread
from time import sleep

from ..Display import *

from .IComponent import *

class CLOCK(IComponent):
    """CLOCK, DEAR TICKING CLOCK"""

    def __init__(self, bus, tick_interval=5):
        super().__init__(bus)

        self.setTickInterval(tick_interval)
        self.stop()

        self.KILL = False
        self.THREAD = None
        self.CALLBACK = lambda: None

    def setTickInterval(self, tick_interval):
        self.TICK_INTERVAL = tick_interval
        return self

    def setTickCallback(self, callback):
        self.CALLBACK = callback
        return self

    def tick(self):
        self.bus.clock()
        self.CALLBACK()
        return self

    def mainloop(self):
        printe('Clock is entering mainloop...')
        while not self.KILL:
            if self.TICKING:
                self.tick()
            sleep(self.TICK_INTERVAL / 1000)
        self.KILL = False
        self.THREAD = None
        printe('Clock has exited mainloop.')
        return self

    def run(self):
        if self.THREAD is None:
            self.THREAD = Thread(target=self.mainloop, name='CLOCK_THREAD')
            self.THREAD.start()
        return self.THREAD

    def start(self):
        self.TICKING = True
        self.run()
        return self

    def stop(self):
        self.TICKING = False
        return self

    def kill(self):
        self.KILL = True
        return self

    def isTicking(self):
        return self.TICKING

    def isThreadStarted(self):
        return self.THREAD is not None
