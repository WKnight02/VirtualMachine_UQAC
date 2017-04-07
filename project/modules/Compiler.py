# -*- coding:utf8 -*-
from .logic.Operation import *

def CompileProgram(commandLines):

		try:
			lineCompile = ''
			line = 0;

			for command in commandLines:
				resultat = Operation.compile(command)
				line += 1

				if resultat == '': continue

				lineCompile += resultat + "\n"

			return (lineCompile, '')

		except Exception as e:
			return ('', str(e) + "\n A la ligne : " + str(line))

def ParsePseudoCompiledProgram(programLines, callback=lambda x:x):
	"""As the "compiled" program consists of integers written as text,
	and the whole system works with Integers, this thing needs to be. Sigh.
	(nb: Better write direct representation as bytes, still needs conversion,
	but its less fuzzy)"""

	for line in programLines:
		if line.strip() == '': continue
		for value in line.split(' '):
			if value.strip() == '': continue
			callback(int(value))
