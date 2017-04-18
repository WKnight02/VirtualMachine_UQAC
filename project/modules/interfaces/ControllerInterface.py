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
		"""
			Cree la fenetre de l'interface
		"""
		# This is the main vertical layout (screen / buttons)
		Pane = tk.PanedWindow(self, orient=tk.HORIZONTAL)

		# Cree les bouttons Play/Pause et le boutton clock mode
		MenuButtons = tk.Frame(Pane)

		self.PlayButton = PlayButton = tk.Button(MenuButtons, text='?', width=5, command=self.onControlPress)
		PlayButton.pack(side=tk.LEFT, fill=tk.Y, expand=1)

		ClockMode = tk.Button(MenuButtons, text='1 Cycle', command=self.onSinglePress)
		ClockMode.pack(side=tk.LEFT, fill=tk.Y, expand=1)

		TickIntervalFrame = tk.Frame(Pane)

		LabelDelayScale = tk.Label(TickIntervalFrame, text='Tick Interval (ms):')
		LabelDelayScale.pack(side=tk.LEFT, fill=tk.Y, expand=1)

		self.DelayScale = DelayScale = tk.Scale(TickIntervalFrame, from_=100, to=0, orient=tk.HORIZONTAL)
		DelayScale.set(5)
		DelayScale.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		self.LabelPC = LabelPC = tk.Label(Pane, text='0', width=50)
		LabelPC.pack(side=tk.RIGHT, fill=tk.Y, expand=1)

		# Display
		Pane.add(MenuButtons)
		Pane.add(TickIntervalFrame)
		Pane.add(LabelPC)
		Pane.pack(side=tk.TOP, fill=tk.BOTH, expand=1, pady=5, padx=5)

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
