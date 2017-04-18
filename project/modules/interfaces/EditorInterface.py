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

	def __init__(this, *args, **kargs):
		"""The ASM editor #TEAMPOULE
		"""
		super().__init__()

		# Sets the size of the interface
		this.height = kargs.get("height", this.DEFAULTS["height"])
		this.width = kargs.get("width", this.DEFAULTS["width"])
		this.geometry("%dx%d" % (this.width, this.height))

		this.create_widgets()

	# Internal function setting up the components/widgets
	def create_widgets(this):
		"""Cree la fenetre de l'interface
		"""
		# This is the main vertical layout (screen / buttons)
		p = tk.PanedWindow(this, orient=tk.VERTICAL)

		#Cree les bouttons enregistrer et charger
		MenuButtons = tk.Frame(this, borderwidth=2, relief=tk.GROOVE)

		LoadButton = tk.Button(MenuButtons, text="Ouvrir", command=this.OpenFile)
		LoadButton.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH)

		SaveButton = tk.Button(MenuButtons, text="Sauvegarder", command=this.SaveFile)
		SaveButton.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH)

		CompileButton = tk.Button(MenuButtons, text="Compiler", command=this.Compile)
		CompileButton.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH)

		ExecuteButton = tk.Button(MenuButtons, text="Executer", command=this.Execute)
		ExecuteButton.pack(side=tk.LEFT, expand=tk.Y, fill=tk.BOTH)

		# Cree la zone d'edition
		this.Input = textEditor = tk.Text(p, background='white')

		#Cree la zone d affichage
		this.resultat = textResultat = tk.Text(p, background='white')
		this.resultat.config(state=tk.DISABLED)

		# Packing
		textEditor.pack(side=tk.RIGHT, fill=tk.Y)
		textResultat.pack(side=tk.RIGHT, fill=tk.Y)

		# Display
		p.add(MenuButtons)
		p.add(textEditor)
		p.add(textResultat)
		p.pack(side=tk.TOP, expand=tk.Y, fill=tk.BOTH, pady=5, padx=5)

	#Save a FILE
	def SaveFile(this):
		"""Enregistre un fichier txt avec le code dans l editeur
		"""
		options = {}
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt')]
		options['initialdir'] = '~/'
		options['initialfile'] = 'fichier.txt'
		options['parent'] = this
		options['title'] = 'Sauvegarder'
		filename = filedialog.asksaveasfilename(**options)
		if filename:
			text = open(filename, 'w')
			data = this.Input.get("1.0",tk.END)
			text.write(data)
			text.close()

	def OpenFile(this):
		"""Ouvre un fichier txt
		"""
		options = {}
		options['defaultextension'] = '.tps'
		options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('TeamPouleSource', '.tps')]
		options['initialdir'] = '~/'
		options['initialfile'] = 'fichier.txt'
		options['parent'] = this
		options['title'] = 'Ouvrir'
		filename = filedialog.askopenfilename(**options)
		if filename:
			text = open(filename, 'r')
			data = text.read()
			text.close()
			this.Input.delete("1.0",tk.END)
			this.Input.insert(tk.END, data)
			this.Input.see(tk.END)


	def Compile(this):
		"""Compile some source
		"""
		Lines = this.Input.get("1.0",tk.END)
		SplitLines = Lines.split("\n")
		compiled, erreur = Compiler.CompileProgram(SplitLines)
		if compiled != '':
			options = {}
			options['defaultextension'] = '.txt'
			options['filetypes'] = [('TeamPouleCompiled', '.tpc')]
			options['initialdir'] = '~/'
			options['initialfile'] = 'Compiled.tpc'
			options['parent'] = this
			options['title'] = 'Sauvegarder'
			filename = filedialog.asksaveasfilename(**options)
			if filename:
				this.ShowResultCompile("Compilation reussi avec succes")
				text = open(filename, 'w')
				text.write(compiled)
				text.close()
		else:
			text = "Erreur de compilation :\n"+erreur
			this.ShowResultCompile(text)

	def ShowResultCompile(this,text):
		"""Afficher le résultat de la compilation
		"""
		this.resultat.config(state=tk.NORMAL)
		this.resultat.delete("1.0",tk.END)
		this.resultat.insert("1.0",text)
		this.resultat.config(state=tk.DISABLED)

	def Execute(this):
		"""Execute some compiled script
		"""
		options = {}
		options['defaultextension'] = '.tpc'
		options['filetypes'] = [('TeamPouleCompiled', '.tpc')]
		options['initialdir'] = '~/'
		options['initialfile'] = 'compiled.tpc'
		options['parent'] = this
		options['title'] = 'Ouvrir'
		filename = filedialog.askopenfilename(**options)

		if filename:
			VM_Module.VirtualMachine.SpawnAndExecute(filename)
