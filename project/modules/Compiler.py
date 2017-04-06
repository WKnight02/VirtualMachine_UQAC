# -*- coding:utf8 -*-

from .logic.Operation import *
def CompileProgram(commands):
		try:
			lineCompile = ''
			line = 0;
			for command in commands:
				line +=1
				resultat = Operation.compile(command)
				if (resultat != ''):
					lineCompile += resultat+"\n"
			return (lineCompile,'') 
		except Exception as e:
			return ('',str(e)+"\n A la ligne : "+str(line))


	