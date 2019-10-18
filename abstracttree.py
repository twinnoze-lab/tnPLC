# -*- coding: utf-8 -*-
# module ladexecution.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is LAD Program Execution.
#
from enum import Enum, auto
import pyparsing as pp


class CommandType(Enum):
    LD = auto()
    AND = auto()
    OR = auto()
    OUT = auto()


class BlockType(Enum):
    BLOCK = auto()  # simple block
    BAND = auto()   # and block
    BOR = auto()    # or block


class Command:
    def __init__(self, cmnd, ope):
        if cmnd[-1] == 'N':
            self.Negative = True
            cmnd = cmnd[:-1]
        else:
            self.Negative = False

        if cmnd == 'LD':
            self.cmnd = CommandType.LD
        elif cmnd == 'AND':
            self.cmnd = CommandType.AND
        elif cmnd == 'OR':
            self.cmnd = CommandType.OR
        elif cmnd == 'OUT':
            self.cmnd = CommandType.OUT
        self.Operand = ope

    def print(self):
        if self.Negative:
            print('  ' + str(self.cmnd) + 'N ' + self.Operand)
        else:
            print('  ' + str(self.cmnd) + ' ' + self.Operand)


class Block:
    def __init__(self):
        self.blocklist = []

    def append(self, block):
        self.blocklist.append(block)

    def pop(self, block):
        return self.blocklist.pop(0)

    def getFirst(self):
        self.index = 0
        if len(self.blocklist) < 1:
            return None
        else:
            return self.blocklist[self.index]

    def getNext(self):
        block = None
        if self.index < len(self.blocklist):
            block = self.blocklist[self.index]
            self.index += 1
        return block

    def print(self):
        count = len(self.blocklist)
        idx = 0

        print('BLOCK >>')
        while idx < count:
            self.blocklist[idx].print()
            idx += 1
        print('<< BLOCK \n')


class BlockComplex:
    def __init__(self, cmnd, first, second):
        self.first = first
        self.second = second
        self.cmnd = cmnd

    def print(self):
        print('BLOCK COMPLEX >> ' + str(self.cmnd))
        if self.first is not None:
            self.first.print()
        if self.second is not None:
            self.second.print()
        print('<< BLOCK COMPLEX ' + str(self.cmnd) + ' \n')


class Network:
    def __init__(self, num):
        self.number = num
        self.block = None
        self.out = None

    def print(self):
        print('NW [' + str(self.number) + '] >>')
        if self.block is not None:
            self.block.print()
        if self.out is not None:
            self.out.print()
        print('\n')


class AbstractTree:

    @classmethod
    def makeAbstractTree(cls, lad):
        try:
            NetworkList = []
            network = None
            ladlen = len(lad)
            idx1 = 0

            # import pdb
            # pdb.set_trace()

            while idx1 < ladlen:
                ladnw = lad[idx1]
                nwlen = len(ladnw)
                idx2 = 0
                while idx2 < nwlen:
                    ladblock = ladnw[idx2]
                    # print(ladblock)
                    if ladblock == 'NW:':
                        idx2 += 1
                        num = ladnw[idx2]
                        network = Network(num)
                        NetworkList.append(network)

                    elif isinstance(ladblock, pp.ParseResults):
                        network.block = cls.makeBlockTree(cls, ladblock)

                    elif ladblock == 'OUT':
                        idx2 += 1
                        op = ladnw[idx2]
                        network.out = Command(ladblock, op)

                    else:
                        pass
                    idx2 += 1
                idx1 += 1

            #cls.print(cls, NetworkList)
        except Exception as er:
            print('Abstract Exception!')

            print(type(er))
            print(er.args)
            print(er)
        return NetworkList

    def makeBlockTree(cls, lad):
        #print('makeBlockTree >>>>>>>>>>>>>')
        block = Block()
        ladlen = len(lad)
        idx1 = 0
        while idx1 < ladlen:
            cmnd = lad[idx1]
            #print(cmnd)
            if isinstance(cmnd, pp.ParseResults):
                bret = cls.makeBlockTree(cls, cmnd)
                block.append(bret )
            if cmnd == 'LD' or cmnd == 'LDN' or cmnd == 'AND' or cmnd == 'ANDN' or cmnd == 'OR' or cmnd == 'ORN':
                idx1 += 1
                op = lad[idx1]
                bret = Command(cmnd, op)
                block.append(bret)

            elif cmnd == 'AND' or cmnd == 'ANDN' or cmnd == 'OR' or cmnd == 'ORN':
                idx1 += 1
                op = lad[idx1]
                block.append(Command(cmnd, op))
            elif cmnd == 'BSAND' or cmnd == 'BSOR':
                pass
            elif cmnd == 'BFAND' or cmnd == 'BFOR':
                #print('BF ::' )

                b1 = block.pop(0)
                b2 = block.pop(0)

                bt = BlockType.BLOCK
                if cmnd == 'BFAND':
                    bt = BlockType.BAND
                elif cmnd == 'BFOR':
                    bt = BlockType.BOR

                bc = BlockComplex(bt, b1, b2)
                block.append(bc)

            idx1 += 1
        #print('<<<<<<<<<<<<<<<<<<< makeblocktree')
        #block.print()
        return block

    def print(cls, nwl):
        cnt = len(nwl)
        idx = 0
        while idx < cnt:
            print(str(idx+1) + '/' + str(cnt))
            nwl[idx].print()
            idx += 1
