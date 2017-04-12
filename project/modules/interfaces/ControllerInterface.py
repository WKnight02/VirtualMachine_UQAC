"""
The Controller's interface
"""
import tkinter as tk
from tkinter import filedialog

__all__ = ['ControllerInterface']

class ControllerInterface(tk.Tk):
	"""Controllers's interface
	"""

	DEFAULTS = {
		"height": 100,
		"width": 450,
	}

	def __init__(this, *args, **kargs):
		"""

		"""
		super().__init__()

		this.buttons = {}
		# Sets the size of the interface
		this.height = kargs.get("height", this.DEFAULTS["height"])
		this.width = kargs.get("width", this.DEFAULTS["width"])
		this.resizable(width=False, height=False)
		this.geometry("%dx%d" % (this.width, this.height))

		this.create_widgets()

	# Internal function setting up the components/widgets
	def create_widgets(this):
		"""
			Cree la fenetre de l'interface
		"""
		# This is the main vertical layout (screen / buttons)
		p = tk.PanedWindow(this, orient=tk.HORIZONTAL)

		#Cree les bouttons Play/Pause et le boutton clock mode
		MenuButtons = tk.Frame(this, borderwidth=2, relief=tk.GROOVE)
		this.PlayButton = PlayButton = tk.Button(MenuButtons, text="Play", command=this.Run)
		PlayButton.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH)

		ClockMode = tk.Button(MenuButtons, text="1 cycle")
		ClockMode.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH)
		champ_label = tk.Label(p, text="Modifier la vitesse:")
		champ_label.pack()
		w = tk.Scale(p, from_=10, to=1, orient=tk.HORIZONTAL)
		w.set(5)
		w.pack()

		# Display
		p.add(MenuButtons)
		p.add(champ_label)
		p.add(w)
		p.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=5, padx=5)

	def Run(this):
		this.PlayButton.config(text="Pause")
		print("Run")
