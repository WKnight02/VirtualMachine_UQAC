# -*- coding:utf8 -*-
import sys

def printe(txt):
    sys.stderr.write(str(txt) + '\n')

def printf(format, *args):
    sys.stdout.write(str(format) % args)

def printfe(format, *args):
    sys.stderr.write(str(format) % args)
