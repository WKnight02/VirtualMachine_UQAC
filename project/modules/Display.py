# -*- coding:utf8 -*-
import sys

"""Various utility print functions"""

def printe(txt):
    """Prints to stderr like 'print' would to stdin"""
    sys.stderr.write(str(txt) + '\n')

def printf(format, *args):
    """C-like printf, no forced line feed"""
    sys.stdout.write(str(format) % args)

def printfe(format, *args):
    """printf, but into stderr"""
    sys.stderr.write(str(format) % args)
