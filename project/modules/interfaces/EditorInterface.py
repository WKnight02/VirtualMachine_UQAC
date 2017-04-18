"""
The editor's interface
"""
from multiprocessing import Process
from tkinter import filedialog
import tkinter as tk
import os

from .. import VirtualMachine as VM_Module
#print(dir())
#print(dir(VM_Module.Compiler))
#VirtualMachine = VM_Module.VirtualMachine # HOLY BLACKMAGIC AAAAAAAAAAH
from .. import Compiler

__all__ = ['EditorInterface']

class EditorInterface(tk.Tk):
	"""Editor's interface
	"""

	DEFAULTS = {
		"height": 650,
		"width": 450,
	}

	def __init__(self, *args, **kargs):
		"""The ASM editor #TEAMPOULE
		"""
		super().__init__()

		# Sets the size of the interface
		self.height = kargs.get("height", self.DEFAULTS["height"])
		self.width = kargs.get("width", self.DEFAULTS["width"])
		self.geometry("%dx%d" % (self.width, self.height))

		self.create_widgets()

	# Internal function setting up the components/widgets
	def create_widgets(self):
		"""Cree la fenetre de l'interface
		"""
		# This is the main vertical layout (screen / buttons)
		Pane = tk.PanedWindow(self, orient=tk.VERTICAL)

		#Cree les bouttons enregistrer et charger
		MenuButtons = tk.Frame(self, padx=5, pady=5)

		LoadButton = tk.Button(MenuButtons, text="Ouvrir", command=self.OpenFile)
		LoadButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		SaveButton = tk.Button(MenuButtons, text="Sauvegarder", command=self.SaveFile)
		SaveButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		CompileButton = tk.Button(MenuButtons, text="Compiler", command=self.Compile)
		CompileButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		ExecuteButton = tk.Button(MenuButtons, text="Executer", command=self.Execute)
		ExecuteButton.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

		# Cree la zone d'edition
		self.Input = textEditor = tk.Text(Pane, background='white', padx=5, pady=5)

		#Cree la zone d affichage
		self.resultat = textResultat = tk.Text(Pane, height=8, background='white', padx=5, pady=5)
		self.resultat.config(state=tk.DISABLED)

		# Packing
		#textEditor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
		#textResultat.pack(side=tk.RIGHT, fill=tk.Y)

		# Display
		Pane.add(textEditor, stretch='always')
		Pane.add(textResultat)

		MenuButtons.pack(side=tk.TOP, fill=tk.X)
		Pane.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

	#Save a FILE
	def SaveFile(self):
		"""Enregistre un fichier txt avec le code dans l editeur
		"""
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = '~/'
		options['initialfile'] = 'fichier.txt'
		options['parent'] = self
		options['title'] = 'Sauvegarder'
		filename = filedialog.asksaveasfilename(**options)
		if filename:
			text = open(filename, 'w')
			data = self.Input.get("1.0",tk.END)
			text.write(data)
			text.close()

	def OpenFile(self):
		"""Ouvre un fichier txt
		"""
		options = {}
		options['defaultextension'] = '.tps'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('TeamPouleSource', '.tps')]
		options['initialdir'] = '~/'
		options['initialfile'] = 'fichier.txt'
		options['parent'] = self
		options['title'] = 'Ouvrir'
		filename = filedialog.askopenfilename(**options)
		if filename:
			text = open(filename, 'r')
			data = text.read()
			text.close()
			self.Input.delete("1.0",tk.END)
			self.Input.insert(tk.END, data)
			self.Input.see(tk.END)


	def Compile(self):
		"""Compile some source
		"""
		Lines = self.Input.get("1.0",tk.END)
		SplitLines = Lines.split("\n")
		compiled, erreur = Compiler.CompileProgram(SplitLines)
		if compiled != '':
			options = {}
			options['defaultextension'] = '.txt'
			options['filetypes'] = [('TeamPouleCompiled', '.tpc')]
			options['initialdir'] = '~/'
			options['initialfile'] = 'Compiled.tpc'
			options['parent'] = self
			options['title'] = 'Sauvegarder'
			filename = filedialog.asksaveasfilename(**options)
			if filename:
				self.ShowResultCompile("Compilation reussi avec succes")
				text = open(filename, 'w')
				text.write(compiled)
				text.close()
		else:
			text = "Erreur de compilation :\n"+erreur
			self.ShowResultCompile(text)

	def ShowResultCompile(self,text):
		"""Afficher le résultat de la compilation
		"""
		self.resultat.config(state=tk.NORMAL)
		self.resultat.delete("1.0",tk.END)
		self.resultat.insert("1.0",text)
		self.resultat.config(state=tk.DISABLED)

	def Execute(self):
		"""Execute some compiled script
		"""
		options = {}
		options['defaultextension'] = '.tpc'
		options['filetypes'] = [('TeamPouleCompiled', '.tpc')]
		options['initialdir'] = '~/'
		options['initialfile'] = 'compiled.tpc'
		options['parent'] = self
		options['title'] = 'Ouvrir'
		filename = filedialog.askopenfilename(**options)

		if filename:
			VM_Module.VirtualMachine.SpawnAndExecute(filename)
