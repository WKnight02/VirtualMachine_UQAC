"""
The Controller's interface
"""
import tkinter as tk
from tkinter import filedialog

__all__ = ['ControllerInterface']

class ControllerInterface(tk.Frame):
	"""Controllers's interface
	"""

	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.create_widgets()

	# Internal function setting up the components/widgets
	def create_widgets(self):
		"""^^"""
		self.PlayButton = PlayButton = tk.Button(self, text='?', width=5, command=self.onControlPress)
		ClockMode = tk.Button(self, text='1 Cycle', command=self.onSinglePress)

		LabelDelayScale = tk.Label(self, text='Tick Interval (ms):')
		self.DelayScale = DelayScale = tk.Scale(self, from_=250, to=0, orient=tk.HORIZONTAL)
		DelayScale.set(5)

		self.LabelPC = LabelPC = tk.Label(self, text='0', width=5)

		# Packing
		PlayButton.pack(side=tk.LEFT, fill=tk.Y)
		ClockMode.pack(side=tk.LEFT, fill=tk.Y)
		LabelDelayScale.pack(side=tk.LEFT, fill=tk.Y)
		DelayScale.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		LabelPC.pack(side=tk.LEFT, fill=tk.Y)

	def setControlledCpu(self, cpu):
		self.cpu = cpu

	def setControlledClock(self, clock):
		self.clock = clock

	def refresh(self):

		# Retrieve the state of the Clock
		if self.clock.isThreadStarted():
			ticking = self.clock.isTicking()
			controlText = 'Stop' if ticking else 'Play'
			relied = tk.SUNKEN if ticking else tk.RAISED
			self.PlayButton.config(text=controlText)
		else:
			self.PlayButton.config(text='...', relief=tk.RAISED)

		# Only setting from refresh
		interval = self.DelayScale.get()
		self.clock.TICK_INTERVAL = interval

		# Retrieve the Program Counter
		currentPC = '0x%04X' % self.cpu.PC
		self.LabelPC.config(text=currentPC)

	def onSinglePress(self):
		self.clock.stop()
		self.clock.tick()
		self.refresh()

	def onControlPress(self):
		if self.clock.isThreadStarted():
			if self.clock.isTicking():
				self.clock.stop()
			else:
				self.clock.start()
		self.refresh()
