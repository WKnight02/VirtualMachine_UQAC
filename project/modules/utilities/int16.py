# -*- coding:utf8 -*-

MAX = 1<<16
MIN = 0

def Overflow(n):
    return (n >= MAX, n % MAX)

def BitGet(n, bit):
    mask = 1 << bit
    return n & mask

def BitSet(n, bit, val):
    mask = 1 << bit
    m = n & (MAX - 1 ^ mask)
    m = m | val << bit
    return m

def Inverse(n):
    return MAX-1 ^ n
