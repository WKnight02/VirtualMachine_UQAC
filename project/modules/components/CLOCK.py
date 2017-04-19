# -*- coding:utf8 -*-
from multiprocessing import Process
from threading import Thread, Event
from time import sleep

from .IComponent import *
from ..interfaces.ControllerInterface import *

class CLOCK(IComponent):
    """CLOCK, DEAR TICKING CLOCK"""

    def __init__(self, bus, tick_interval=5):
        super().__init__(bus)

        self.setTickInterval(tick_interval)
        self.stop()

        self.KILL = Event()
        self.THREAD = None
        self.ON_KILL = lambda: None

    def setTickInterval(self, tick_interval): # Should not be < 0 huehuehue
        self.TICK_INTERVAL = max(tick_interval, 0.001)
        return self

    def setKillCallback(self, callback):
        self.ON_KILL = callback
        return self

    def tick(self):
        """Trigger 1 CPU cycle"""
        infos = self.bus.clock()

        # Actually stops if receiving halt signal from cpu
        return ('cpu', 'halt') in infos

    def mainloop(self):
        """This is where all the magic happens:
        It is the loop started in the parallel thread."""

        # While we are allowed to live:
        while not self.KILL.is_set():

            # If we are allowed to tick
            if self.TICKING:

                # If tick() return True, lets stop our stuff
                if self.tick():
                    self.KILL.set()
                    break

            # Tick Interval
            sleep(self.TICK_INTERVAL / 1000)

        # We got out of the loop, time to clean state properties
        self.KILL.clear()
        self.TICKING = False
        self.THREAD = None

        # We are getting out, time to callback !
        self.ON_KILL()
        return

    def run(self):
        """This starts the parallel thread, but does not modify the clocks
        state (such as start/stop)"""
        if self.THREAD is None:
            self.THREAD = Thread(target=self.mainloop)
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

    def kill(self, join=False):
        """This does really stop everything: stop the ticking + thread"""
        self.KILL.set()
        if join: self.THREAD.join()
        return self

    def isTicking(self):
        """Is the clock allowed to tick ?"""
        return self.TICKING

    def isThreadStarted(self):
        """Is the parallel thread running ?"""
        return self.THREAD is not None or self.THREAD.isAlive()
