# -*- coding:utf8 -*-
from .IComponent import *
from .ALU import *

class CPU(IComponent):
    """CENTRAL PROCESSING UNIT"""

    def __init__(self, bus):
        super().__init__(bus)
        self.ALU = ALU()

        # A B C D
        self.REGISTERS = [0 for i in range(4)]

        # S, P et I
        self.STATE = 0
        self.PC = 0
        self.IR = 0

    def getRegister(self, reg):
        """Register is from 0x01 to 0x04,
        but indices range from 0 to 3..."""
        i = reg - 1
        if i < 0 or i > 3:
            raise ValueError('Register at 0x%x is invalid' % reg)
        return self.REGISTERS[i]

    def getShared(self, adr):
        """Get data through the BUS"""
        pass

    def fetch(self):
        pass

    def decode(self):
        pass

    def execute(self):
        pass

    def clock(self):
        self.fetch()
        self.decode()
        self.execute()

    # MEGA DEF OF DOOM
    def invoke(self, method):
        """CPU_OBJECT.invoke(OP)(*args)"""
        try:
            return getattr(self, method.upper())
        except AttributeError: # Empty function
            return lambda *args, **kargs: None

    def Managed(*types, store=None):
        """This ensure each function affects correctly the different CPU registers.
        Also allows for fuzzy arguments conversion.
        Types:
         - r, reg, register
         - a, adr, address
         - v, val, value
        """

        TYPES = {
            'register': ('r', 'reg', 'register'),
            'address': ('a', 'adr', 'address'),
            'value': ('v', 'val', 'value', None),
        }

        def decorator(func):
            """The actual decorator"""

            def modified(self, *args):
                """Decorated _INSTANCE_ function"""

                # Argument conversion based on 'types'
                cargs = []
                for i in range(len(types)):
                    carg = args[i]
                    T = types[i]

                    if T in TYPES['register']:
                        carg = self.getRegister(carg)

                    elif T in TYPES['address']:
                        carg = self.getShared(carg)

                    elif T not in TYPES['value']:
                        raise TypeError('Managed type is invalid [%s]' % T)

                    cargs.append(carg)

                # Complete the rest
                cargs += args[i+1:]

                # Call with converted args the function
                value = func(*cargs)

                # Check for overflow
                if value > 65536:
                    value %= 65536

                if stored is not None:
                    i = stored - 1
                    if types[i] not in TYPES['register']:
                        raise TypeError("Can't store your shit")
                    self.setRegister(args[i], value)

                return value

            return modified

        return decorator

    @Managed('r', 'r', store=1)
    def ADD(self, reg1, reg2): return reg1 + reg2

    @Managed('r', 'r', store=1)
    def SUB(self, reg1, reg2): return reg1 - reg2

    @Managed('r', 'r', store=1)
    def MUL(self, reg1, reg2): return reg1 * reg2

    @Managed('r', 'r', store=1)
    def DIV(self, reg1, reg2): return reg1 / reg2

    @Managed('a')
    def JMP(self, adr):
        self.IR = adr
        return adr
