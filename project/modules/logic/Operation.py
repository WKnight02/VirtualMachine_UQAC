# -*- coding:utf8 -*-

class Operation(object):

    DEFINED = {
        'DTA':  (0, 'val'),

        'JMP':  (0x0100, None, 0, 'adr'),
        'JMZ':  (0x0200, None, 0, 'adr'),
        'JMO':  (0x0300, None, 0, 'adr'),
        'JMC':  (0x0400, None, 0, 'adr'),

        'SET':  (0x0500, 'reg', 0, 'val'),
        'LD':   (0x0600, 'reg', 0, 'val'),
        'ST':   (0x0700, 'reg', 0, 'adr'),
        'MV':   (0x0800, 'reg', 0, 'reg'),

        'ADD':  (0x1100, 'reg', 0, 'reg'),
        'SUB':  (0x1200, 'reg', 0, 'reg'),
        'MUL':  (0x1300, 'reg', 0, 'reg'),
        'DIV':  (0x1400, 'reg', 0, 'reg'),

        'OR':   (0x2100, 'reg', 0, 'reg'),
        'AND':  (0x2200, 'reg', 0, 'reg'),
        'XOR':  (0x2300, 'reg', 0, 'reg'),
        'NOT':  (0x2400, 'reg'),

        'LT':   (0x3100, 'reg', 0, 'val'),
        'GT':   (0x3200, 'reg', 0, 'val'),
        'LE':   (0x3300, 'reg', 0, 'val'),
        'GE':   (0x3400, 'reg', 0, 'val'),
        'EQ':   (0x3500, 'reg', 0, 'val'),
        'EZ':   (0x3600, 'reg'),
        'NZ':   (0x3700, 'reg'),
    }

    def __init__(self, BASECODE, *args): pass
    # phew. need more thinkin.

    @staticmethod
    def compile(source):
        pass
