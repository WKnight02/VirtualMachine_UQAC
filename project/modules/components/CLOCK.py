# -*- coding:utf8 -*-
from multiprocessing import Process
from threading import Thread
from time import sleep

from .IComponent import *
from ..interfaces.ControllerInterface import * 

class CLOCK(IComponent):
    """CLOCK, DEAR TICKING CLOCK"""

    def __init__(self, bus, tick_interval=5):
        super().__init__(bus)

        self.setTickInterval(tick_interval)
        self.stop()

        self.KILL = False
        self.THREAD = None
        self.CALLBACK = lambda: None

    def setTickInterval(self, tick_interval): # Should not be < 0 huehuehue
        self.TICK_INTERVAL = min(tick_interval, 0)
        return self

    def setTickCallback(self, callback):
        """Sets some callback function to be called on each tick()"""
        self.CALLBACK = callback
        return self

    def tick(self):
        """Trigger 1 CPU cycle"""
        infos = self.bus.clock()
        self.CALLBACK()

        # Actually stops if receiving halt signal from cpu
        return ('cpu', 'halt') in infos

    def mainloop(self):
        """This is where all the magic happens:
        It is the loop started in the parallel thread."""


        # While we are allowed to live:
        while not self.KILL:

            # If we are allowed to tick
            if self.TICKING:

                # If tick() return True, lets stop our stuff
                self.KILL = self.tick()

            # Tick Interval
            sleep(self.TICK_INTERVAL / 1000)

        # We got out of the loop, time to clean state properties
        self.KILL = False
        self.TICKING = False
        self.THREAD = None

        return self

    def run(self):
        """This starts the parallel thread, but does not modify the clocks
        state (such as start/stop)"""
        if self.THREAD is None:
            self.THREAD = Thread(target=self.mainloop, name='CLOCK_THREAD')
            self.THREAD.start()
        return self.THREAD

    def start(self):
        """Actually starts the clock and the thread if not already started"""
        self.TICKING = True
        self.run()
        return self

    def stop(self):
        """Only stops the ticking, the clock is still alive, just not triggering"""
        self.TICKING = False
        return self

    def kill(self):
        """This does really stop everything: stop the ticking + thread"""
        self.KILL = True
        return self

    def isTicking(self):
        """Is the clock allowed to tick ?"""
        return self.TICKING

    def isThreadStarted(self):
        """Is the parallel thread running ?"""
        return self.THREAD is not None