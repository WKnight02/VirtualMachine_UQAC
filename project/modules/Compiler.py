# -*- coding:utf8 -*-

from .logic.Operation import *
def CompileProgram(commands):
		try:
			lineCompile = ''
			for command in commands:
				lineCompile += Operation.compile(command)+"n"
			return lineCompile
		except Exception as e:
			print(e)


	