# -*- coding:utf8 -*-
import project.modules.ArgParser as ArgParser

from project.modules.VirtualMachine import *

filename = ArgParser.getArg('file', ArgParser.getPos(1))
if filename is None: raise Exception('First argument must be the compiled file to run.')

VirtualMachine.SpawnAndExecute(filename)
