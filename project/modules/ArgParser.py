# -*- coding:utf8 -*-
import sys

KARGS = {}

pos = 0
for arg in sys.argv[1:]:
    split = arg.split(':', 2)

    if len(split) < 2:
        KARGS[pos] = arg
        pos += 1

    else: KARGS[split[0]] = split[1]
# END FOR

def getArg(key, default=None):
    return KARGS.get(key, default)

def getPos(position, default=None):
    return sys.argv[position] if 0 <= position < len(sys.argv) else default
