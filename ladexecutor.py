# -*- coding: utf-8 -*-
# module ladexecution.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is LAD Program Execution.
#
import abstracttree as at


class LADExecutor:
    """tnPLC LAD Program Execution"""

    def __init__(self, memmng):
        self.memmng = memmng

    def Execution(self, abtree):
        nwcnt = len(abtree)
        idx = 0

        while idx < nwcnt:
            network = abtree[idx]

            # Execute Network Main Block
            num = network.number
            #print('\nExecution NW:' + str(num))
            ret = self.execBlock(network.block)
            #print('ret ::' + str(ret))
            ope = network.out.Operand
            self.memmng.setMemory(ope, ret)

            idx += 1
        return

    def execBlock(self, block):
        state = True
        mem = True
        blocklen = len(block.blocklist)
        idx = 0

        #block.print()
        #print('In ExecBlock >>>>>')
        #block.print()
        #print('######################')
        while idx < blocklen:
            cmnd = block.blocklist[idx]
            if isinstance(cmnd, at.BlockComplex):
                mem = self.execBlockComplex(cmnd)
            elif cmnd.cmnd == at.CommandType.LD:
                ope = cmnd.Operand
                if cmnd.Negative:
                    mem = not self.memmng.getMemory(ope)
                else:
                    mem = self.memmng.getMemory(ope)
                #print('CommandType.LD:  ' + ope + ' : ' + str(mem))
            elif cmnd.cmnd == at.CommandType.AND:
                state &= mem
                ope = cmnd.Operand
                if cmnd.Negative:
                    mem = not self.memmng.getMemory(ope)
                else:
                    mem = self.memmng.getMemory(ope)
                #print('CommandType.AND:  ' + ope + ' : ' + str(mem))
            elif cmnd.cmnd == at.CommandType.OR:
                ope = cmnd.Operand
                if cmnd.Negative:
                    mem = mem | (not self.memmng.getMemory(ope))
                else:
                    mem = mem | self.memmng.getMemory(ope)
                #print('CommandType.OR:  ' + ope + ' : ' + str(mem))
            idx += 1

        state &= mem
        #print('Out ExecBlock <<<<<< + state::' + str(state))
        return state

    def execBlockComplex(self, cmplex):

        #print('In ExecBlockComplex >>>>>')
        if isinstance(cmplex, at.BlockComplex):
            ret1 = True
            ret2 = True
            if isinstance(cmplex.first, at.BlockComplex):
                ret1 = self.execBlockComplex(cmplex.first)
            elif isinstance(cmplex.first, at.Block):
                ret1 = self.execBlock(cmplex.first)
            #print('ret1 ::' + str(ret1))
            if isinstance(cmplex.second, at.BlockComplex):
                ret2 = self.execBlockComplex(cmplex.second)
            elif isinstance(cmplex.second, at.Block):
                ret2 = self.execBlock(cmplex.second)
            #print('ret2 ::' + str(ret2))

            state = True
            if cmplex.cmnd == at.BlockType.BLOCK or cmplex.cmnd == at.BlockType.BAND:
                state = ret1 & ret2
            elif cmplex.cmnd == at.BlockType.BOR:
                state = ret1 | ret2

            #print('Out ExecBlockComplex <<<<<< + state::' + str(state))
            return state
        else:
            print('Error from ExecBlockComplex!')
            return None

