# -*- coding:utf8 -*-
import re

class CompilationError(Exception): pass

class Operation(object):

    DEFINED = {
        'DTA':  (0, 'val'),


        'SET':  (0x0500, 'reg', 'val'),
        'LD':   (0x0600, 'reg', 'spc'),
        'ST':   (0x0700, 'reg', 'spc'),
        'MV':   (0x0800, 'reg', 'reg'),

        'ADD':  (0x1100, 'reg', 'reg'),
        'SUB':  (0x1200, 'reg', 'reg'),
        'MUL':  (0x1300, 'reg', 'reg'),
        'DIV':  (0x1400, 'reg', 'reg'),

        'OR':   (0x2100, 'reg', 'reg'),
        'AND':  (0x2200, 'reg', 'reg'),
        'XOR':  (0x2300, 'reg', 'reg'),
        'NOT':  (0x2400, 'reg'),

        'LT':   (0x3100, 'reg', 'reg'),
        'GT':   (0x3200, 'reg', 'reg'),
        'LE':   (0x3300, 'reg', 'reg'),
        'GE':   (0x3400, 'reg', 'reg'),
        'EQ':   (0x3500, 'reg', 'reg'),
        'EZ':   (0x3600, 'reg'),
        'NZ':   (0x3700, 'reg'),

        'JMP':  (0x0100, 'adr'),
        'JMZ':  (0x0200, 'adr'),
        'JMO':  (0x0300, 'adr'),
        'JMC':  (0x0400, 'adr'),

        'NOP':  (0x0000,),
        'HLT':  (0x0F00,)
    }

    REGISTER = {
        "A": 0x01,
        "B": 0x02,
        "C": 0x03,
        "D": 0x04,
    }

    def __init__(self, BASECODE, *args): pass
    # phew. need more thinkin.

    @classmethod
    def computeReverseLookup(cls):
        reverse = {}
        for op, params in cls.DEFINED.items():
            reverse[params[0]] = (op,) + params[1:]
        return reverse

    @classmethod
    def compile(cls, source):
        command = source.split(" ")
        while command.count(''): del command[command.index('')]
        if len(command) != 0:
            '''
            TEST DTA
            '''
            if command[0] == "DTA":
                arg = ' '.join(command[1:])
                parsed = None
                compiled =[]

                try:
                    parsed = int(arg)
                    return '%d' % (parsed)
                except:
                    try:

                        p = re.compile('^".*"$')
                        if p.match(arg) is None:
                            raise CompilationError("Argument incorrect")

                        else:
                            parsed = arg[1:-1]
                            for c in parsed:
                                compiled.append(str(ord(c)))
                            return ' '.join(compiled)

                    except Exception as e:
                        raise e


            '''
            AUTRE Operation
            '''
            Op = cls.DEFINED[str(command[0])]

            #Test les operation sans argument
            if len(command) == 1 and (command[0] == "NOP" or command[0] == "HLT")  :
                return '%d' % (Op[0])

            elif len(command[1:]) == len(Op)-1:

                #Test si le premier argument attendu est bien le bon ici registre
                if Op[1] == 'reg' and command[1] in 'ABCD':

                    if len(command)>2:
                        if Op[2] == 'reg' and command[2] in 'ABCD':
                            int1 = Op[0]+cls.REGISTER[str(command[1])]
                            int2 = 0x0000 + cls.REGISTER[str(command[2])]
                            return '%d %d' % (int1,int2)

                        elif Op[2] == 'adr' or Op[2] == 'val':
                            try:
                                int2 = int(command[2],0)
                                int1 = Op[0]+cls.REGISTER[str(command[1])]
                                return '%d %d' % (int1,int2)
                            except:
                                raise CompilationError('Argument non valide: Adresse ou valeur attendu')
						#Operation ST et LD
                        elif Op[2] == 'spc':
                            if command[2] in 'ABCD':
                                int1 = (Op[0]+cls.REGISTER[str(command[1])]) | 0x0010
                                int2 = 0x0000 + cls.REGISTER[str(command[2])]
                            else:
                                try:
                                    int1 = Op[0]+cls.REGISTER[str(command[1])]
                                    int2 = int(command[2],0)
                                except:
                                    raise CompilationError('Argument non valide')
                            return '%d %d' % (int1,int2)
                        else:
                            raise CompilationError('Argument non valide: Registre attendu')

                    else:
                        int1 = Op[0]+cls.REGISTER[str(command[1])]
                        return '%d' % (int1)

                #Test si le premier argument attendu est bien le bon ici une adresse
                elif Op[1] == 'adr':
                    try:
                        int1 = Op[0]
                        int2 = int(command[1],0)
                        return '%d %d' % (int1,int2)

                    except:
                        raise CompilationError('Argument non valide: Adresse attendu')

                #Si Op[1] == 'reg' mais que l argument n est pas un registre
                else :
                    raise CompilationError('Argument non valide: Registre attendu')

            else:
                raise CompilationError("Nombre d'argument incorrect")

        else:
            return '';
