# -*- coding:utf8 -*-
from ..Display import *

from ..utilities import int16
from ..logic.Operation import *
from .IComponent import *
from .ALU import *

# Store the unmodified CPU functions, just in case.
CPU_OPERATIONS = {}

class CpuError(Exception): pass
class DecodingError(CpuError): pass
class ExecutionError(CpuError): pass

class CPU(IComponent):
    """CENTRAL PROCESSING UNIT"""

    STATE_PARITY = 0
    STATE_SIGN = 1
    STATE_CARRY = 2
    STATE_ZERO = 3
    STATE_CND = 4

    # Is the execution halted ?
    STATE_HALT = 15

    OPERATION_LOOKUP = Operation.computeReverseLookup()

    def __init__(self, bus):
        super().__init__(bus)
        self.ALU = ALU() # Inutile dans notre implémentation ?
        self.initRegisters()

    def initRegisters(self):
        """The initialization"""

        # A B C D
        self.REGISTERS = [0 for i in range(4)]

        # S, P et I
        self.STATE = 0
        self.PC = 0
        self.IR = 0

    def getStateBit(self, bit):
        return int16.BitGet(self.STATE, bit)

    def setStateBit(self, bit, val):
        self.STATE = int16.BitSet(self.STATE, bit, val)
        return self

    def getRegister(self, reg):
        """Register is from 0x01 to 0x04,
        but indices range from 0 to 3..."""
        i = reg - 1
        if i < 0 or i > 3:
            raise ValueError('Register at 0x%x is invalid' % reg)
        return self.REGISTERS[i]

    def setRegister(self, reg, val):
        i = reg - 1
        self.REGISTERS[i] = val
        return self

    def getShared(self, adr):
        """Get data through the BUS"""
        return self.bus.read(adr)

    def setShared(self, adr, val):
        """Set data through the BUS"""
        return self.bus.write(adr, val)

    def fetch(self):
        """Current instruction"""
        self.IR = self.getShared(self.PC)
        if self.IR is None:
            self.IR = Operation.DEFINED['HLT'][0]
        return self.IR

    def decode(self):
        """Decoding OPCODE"""
        code = self.IR
        opcode = code & 0xFF00

        if opcode not in self.OPERATION_LOOKUP:
            raise DecodingError('Unknown opcode "0x%04X" at [0x%04X]' % (opcode, self.PC))
        self.PC += 1

        operation, *params = self.OPERATION_LOOKUP[opcode]
        psize = len(params)
        decoded = []

        # Instruction doesnt require parameters
        if psize == 0:
            pass

        # Instruction has at least one operator
        elif psize >= 1:

            if params[0] == 'reg':
                decoded.append(self.IR & 0x00FF)

            elif params[0] == 'adr':
                decoded.append(self.fetch())
                self.PC += 1

            if psize == 2:

                arg = self.fetch()

                # Do we read the arg value 'as if' or do we read it from register ?
                if params[1] == 'spc' and code & 0x0010:
                    arg = self.getRegister(arg)

                decoded.append(arg)
                self.PC += 1

        return operation, decoded

    def execute(self, operation, args):
        """Tries to execute the operation with its decoded arguments"""
        try:
            return self.invoke(operation)(*args)
        except Exception as e:
            raise ExecutionError(
                '\n > An error occured while processing instruction 0x%04X[%s] at [0x%04X]...\n Error: %s' % (
                    self.IR, operation, self.PC, str(e))
                )

    def clock(self):

        # Do nothing if program halted.
        if self.getStateBit(self.STATE_HALT): return ('cpu', 'halt')
        #printf('\r0x%04X', self.PC)

        # Fetch, decode, execute.
        self.fetch()
        operation, args = self.decode()
        self.execute(operation, args)
        return

    # MEGA DEF OF DOOM
    def invoke(self, method):
        """CPU_OBJECT.invoke(OP)(*args)"""
        try:
            return getattr(self, method.upper())
        except AttributeError: # Empty function
            return lambda *args, **kargs: None

    def Managed(*types, store=None, status=None):
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

        def decorator(method):
            """The actual decorator"""

            def modified(self, *args):
                """Decorated _INSTANCE_ function"""

                # Argument conversion based on 'types'
                cargs = []
                for i in range(len(types)):
                    carg = args[i]
                    T = types[i]

                    if T in TYPES['register']:
                        carg = self.getRegister(carg & 0xF)

                    elif T in TYPES['address']:
                        carg = self.getShared(carg)

                    elif T not in TYPES['value']:
                        raise TypeError('Managed type is invalid [%s]' % T)

                    cargs.append(carg)

                # Complete the rest
                cargs += args[i+1:]

                # Call with converted args the function
                value = method(self, *cargs)
                if value is None: value = 1

                # Check sign
                sign = 0
                if value < 0:
                    value = abs(value)
                    sign = 1
                self.setStateBit(self.STATE_CARRY, sign)

                # Check for overflow
                overflow, cleanValue = int16.Overflow(value)
                self.setStateBit(self.STATE_CARRY, int(overflow))

                # Check for zero
                self.setStateBit(self.STATE_ZERO, int(cleanValue == 0))

                # Check for parity
                parity = int16.BitGet(cleanValue, 0)
                self.setStateBit(self.STATE_PARITY, parity)

                if status is not None:
                    self.setStateBit(status, cleanValue)

                if store is not None:
                    i = store - 1
                    if types[i] not in TYPES['register']:
                        raise TypeError("Can't store your shit")
                    self.setRegister(args[i], cleanValue)

                return value

            # Enregistrement de la fonction modifiée
            CPU_OPERATIONS[method.__name__] = method
            return modified

        return decorator

    ###
    # Data manipulation

    @Managed('r', 'v', store=1)
    def SET(self, reg, val): return val

    @Managed('r', 'a', store=1)
    def LD(self, reg, adr): return adr

    @Managed('r', 'v') # Little hack for setting distant address
    def ST(self, reg, adr): self.setShared(adr, reg)

    @Managed('r', 'r', store=1)
    def MV(self, reg1, reg2): return reg2

    ###
    # Comparisons

    @Managed('r', 'r', status=STATE_CND)
    def LT(self, reg1, reg2): return int(reg1 < reg2)

    @Managed('r', 'r', status=STATE_CND)
    def GT(self, reg1, reg2): return int(reg1 > reg2)

    @Managed('r', 'r', status=STATE_CND)
    def LE(self, reg1, reg2): return int(reg1 <= reg2)

    @Managed('r', 'r', status=STATE_CND)
    def GE(self, reg1, reg2): return int(reg1 >= reg2)

    @Managed('r', 'r', status=STATE_CND)
    def EQ(self, reg1, reg2): return int(reg1 == reg2)

    @Managed('r', status=STATE_CND)
    def EZ(self, reg1): return int(reg1 == 0)

    @Managed('r', status=STATE_CND)
    def NZ(self, reg1): return int(reg1 != 0)

    ###
    # Logic

    @Managed('r', 'r', store=1)
    def OR(self, reg1, reg2): return reg1 | reg2

    @Managed('r', 'r', store=1)
    def AND(self, reg1, reg2): return reg1 & reg2

    @Managed('r', 'r', store=1)
    def XOR(self, reg1, reg2): return reg1 ^ reg2

    @Managed('r', store=1)
    def NOT(self, reg1): return int16.Inverse(reg1)

    ###
    # Basic operations

    @Managed('r', 'r', store=1)
    def ADD(self, reg1, reg2): return reg1 + reg2

    @Managed('r', 'r', store=1)
    def SUB(self, reg1, reg2): return reg1 - reg2

    @Managed('r', 'r', store=1)
    def MUL(self, reg1, reg2): return reg1 * reg2

    @Managed('r', 'r', store=1)
    def DIV(self, reg1, reg2): return reg1 / reg2

    ###
    # Flow control

    @Managed('v')
    def JMP(self, adr):
        self.PC = adr
        return adr

    @Managed('v')
    def JMZ(self, adr):
        if self.getStateBit(self.STATE_ZERO):
            self.PC = adr
        return adr

    @Managed('v')
    def JMO(self, adr):
        if self.getStateBit(self.STATE_CARRY):
            self.PC = adr
        return adr

    @Managed('v')
    def JMC(self, adr):
        if self.getStateBit(self.STATE_CND):
            self.PC = adr
        return adr

    # \o/
    def NOP(self): return
    def HLT(self):
        self.setStateBit(self.STATE_HALT, 1)
