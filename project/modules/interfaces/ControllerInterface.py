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
		"""Create the differents element of the screen"""
		self.PlayButton = PlayButton = tk.Button(self, text='?', width=5, padx=5, command=self.onControlPress)
		ClockMode = tk.Button(self, text='1 Cycle', command=self.onSinglePress, bg='#AAF')

		LabelDelayScale = tk.Label(self, text='Tick Interval (ms):')
		self.DelayScale = DelayScale = tk.Scale(self, from_=250, to=0, orient=tk.HORIZONTAL)
		DelayScale.set(5)

		self.LabelPC = LabelPC = tk.Label(self, text='0')

		self.ResetPC = ResetPC = tk.Button(self, text='R', bg='#FAA', fg='#FFF', command=self.onReset)
		# Packing
		PlayButton.pack(side=tk.LEFT, fill=tk.Y)
		ClockMode.pack(side=tk.LEFT, fill=tk.Y)
		LabelDelayScale.pack(side=tk.LEFT, fill=tk.Y)
		DelayScale.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
		LabelPC.pack(side=tk.LEFT, fill=tk.Y)
		ResetPC.pack(side=tk.LEFT, fill=tk.Y)
	def setControlledVM(self, vm):
		"""Binds VM's components to the controls"""
		self.vm = vm
	def refresh(self):
		"""Update everything on the UI"""

		# Is the thread running ?
		if self.vm.clock.isThreadStarted():

			# Is the cpu in HALT mode ?
			if self.vm.cpu.getStateBit(self.vm.cpu.STATE_HALT):
				controlText = 'HALTED'
				relief = tk.FLAT
				color = '#FA6'

			# Nope, its cycling !
			else:
				ticking = self.vm.clock.isTicking()
				controlText = 'Stop' if ticking else 'Play'
				relief = tk.SUNKEN if ticking else tk.RAISED
				color = '#F66' if ticking else '#6F6'

			self.PlayButton.config(text=controlText, relief=relief, bg=color, fg='#000')
		else:
			self.PlayButton.config(text='KILLED', relief=tk.RAISED, bg='#000', fg='#FFF')

		# Only setting from refresh
		interval = self.DelayScale.get()
		self.vm.clock.setTickInterval(interval)

		# Retrieve the Program Counter
		currentPC = 'PC: 0x%04X' % self.vm.cpu.PC
		self.LabelPC.config(text=currentPC)

	def onSinglePress(self):
		"""Action when clicked on the 'do just 1 Cycle' button..."""
		self.vm.clock.stop()
		self.vm.clock.tick()
		self.refresh()

	def onControlPress(self):
		"""Action when pressing the control button (play/pause)"""
		if self.vm.clock.isThreadStarted():
			if self.vm.clock.isTicking():
				self.vm.clock.stop()
			else:
				self.vm.clock.start()
		self.refresh()

	def onReset(self):
		"""Resets the VM to its Zero-state. We hope."""
		self.vm.restart()
		self.refresh()
