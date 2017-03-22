# -*- coding:utf8 -*-

class Operation(object):

    DEFINED = {
        'DTA':  Operation(0, 'val'),

        'JMP':  Operation(0x0100, None, 0, 'adr'),
        'JMZ':  Operation(0x0200, None, 0, 'adr'),
        'JMO':  Operation(0x0300, None, 0, 'adr'),
        'JMC':  Operation(0x0400, None, 0, 'adr'),

        'SET':  Operation(0x0500, 'reg', 0, 'val'),
        'LD':   Operation(0x0600, 'reg', 0, 'val'),
        'ST':   Operation(0x0700, 'reg', 0, 'adr'),
        'MV':   Operation(0x0800, 'reg', 0, 'reg'),

        'ADD':  Operation(0x1100, 'reg', 0, 'reg'),
        'SUB':  Operation(0x1200, 'reg', 0, 'reg'),
        'MUL':  Operation(0x1300, 'reg', 0, 'reg'),
        'DIV':  Operation(0x1400, 'reg', 0, 'reg'),

        'OR':   Operation(0x2100, 'reg', 0, 'reg'),
        'AND':  Operation(0x2200, 'reg', 0, 'reg'),
        'XOR':  Operation(0x2300, 'reg', 0, 'reg'),
        'NOT':  Operation(0x2400, 'reg'),

        'LT':   Operation(0x3100, 'reg', 0, 'val'),
        'GT':   Operation(0x3200, 'reg', 0, 'val'),
        'LE':   Operation(0x3300, 'reg', 0, 'val'),
        'GE':   Operation(0x3400, 'reg', 0, 'val'),
        'EQ':   Operation(0x3500, 'reg', 0, 'val'),
        'EZ':   Operation(0x3600, 'reg'),
        'NZ':   Operation(0x3700, 'reg'),
    }

    def __init__(BASECODE, *args): pass
    # phew. need more thinkin.
