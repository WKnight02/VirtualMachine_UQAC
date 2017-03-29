# -*- coding:utf8 -*-

class Operation(object):

    DEFINED = {
        'DTA':  (0, 'val'),


        'SET':  (0x05, 'reg', 0, 'val'),
        'LD':   (0x06, 'reg', 0, 'val'),
        'ST':   (0x07, 'reg', 0, 'adr'),
        'MV':   (0x08, 'reg', 0, 'reg'),

        'ADD':  (0x11, 'reg', 0, 'reg'),
        'SUB':  (0x12, 'reg', 0, 'reg'),
        'MUL':  (0x13, 'reg', 0, 'reg'),
        'DIV':  (0x14, 'reg', 0, 'reg'),

        'OR':   (0x21, 'reg', 0, 'reg'),
        'AND':  (0x22, 'reg', 0, 'reg'),
        'XOR':  (0x23, 'reg', 0, 'reg'),
        'NOT':  (0x24, 'reg'),

        'LT':   (0x31, 'reg', 0, 'val'),
        'GT':   (0x32, 'reg', 0, 'val'),
        'LE':   (0x33, 'reg', 0, 'val'),
        'GE':   (0x34, 'reg', 0, 'val'),
        'EQ':   (0x35, 'reg', 0, 'val'),
        'EZ':   (0x36, 'reg'),
        'NZ':   (0x37, 'reg'),

        'JMP':  (0x01, 'adr'),
        'JMZ':  (0x02, 'adr'),
        'JMO':  (0x03, 'adr'),
        'JMC':  (0x04, 'adr'),

        'NOP':  (0x00,),
        'HLT':  (0x0F,)
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
    def compile(cls, source):
        command = source.split(" ")
        while command.count(''): del command[command.index('')]
        if len(command) != 0:
            Op = cls.DEFINED[str(command[0])]
            if command[0] == "NOP" or command[0] == "HLT" and len(command) == 1:
                return bytes((Op[0],0x00))
            elif len(command[1:]) == len(Op)/2:
                if Op[1] == 'reg' and command[1] in 'ABCD':        
                    if len(command)>2:
                        if Op[3] == 'reg' and command[1] in 'ABCD':
                            return bytes((Op[0],cls.REGISTER[str(command[1])],0x00,cls.REGISTER[str(command[2])]))
                        elif Op[3] == 'adr' or Op[3] == 'val':
                            val = int(command[2],0)
                            print (val)
                            return bytes((Op[0],cls.REGISTER[str(command[1])]))+ val.to_bytes(2,'big')
                        else:
                            return None;
                    else:
                        return bytes((Op[0],cls.REGISTER[str(command[1])]))
                elif Op[1] == 'adr':
                    try:
                        val = int(command[1],0)
                        return (bytes((Op[0],0x00)) + val.to_bytes(2,'big'))
                    except:
                        print("argument non valide: Adr attendu")
                        return None
                else :
                    print("argument non valide: Registre attendu")
                    return None;
            else:
                print("Nombre d'argument incorrect")
                return None;
        else:
            print("Ligne Vide")
            return bytes ()


Text = "NOP A"
print(Operation.compile(Text))
