# -*- coding: utf-8 -*-
# module tnplc.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is main program of the tnPLC
#
import sys

import rpgpio
import memmng
import ladparser
import cycletimectrl
import processinfo


def getVersion():
    """tnPLC Project version"""
    return 'v0.0.3'

class tnPLC:
    """tnPLC main"""

    # constructor
    def __init__(self):
        self.ladparser = ladparser.LADParser()
        # initialize memory manager
        self.memmng = memmng.MemManage()
        self.lad = 0
        # initialize GPIO
        self.gpio = rpgpio.RpGPIO()
        # process inpormation write out
        self.procinfo = processinfo.ProcessInfo()

    def start(self):
        """tnPLC startup point"""

        """read argument"""
        args = sys.argv

        """read LAD file"""
        self.lad = self.ladparser.parseFile(args[1])
        if self.lad is None:
            print('LAD File[', args[1], '] Parse Errer!')
        else:
            # LAD program start
            self.run()

        """cleanup GPIO"""
        self.gpio.finish()
        return

    def run(self):
        """cyclic RUN"""
        try:
            self.ctc = cycletimectrl.CycleTimeCtrl()
            self.isRoop = True

            while self.isRoop:
                self.inputRefuresh()
                self.cyclic()
                self.outputRefuresh()
                self.sleep()
        except KeyboardInterrupt:
            self.isRoop = False
          

    def inputRefuresh(self):
        """refresh GPIO Input"""
        self.memmng.refreshInput(self.gpio)

    def outputRefuresh(self):
        """refresh GPIO Output"""
        self.memmng.refreshOutput(self.gpio)

    def cyclic(self):
        """LAD process"""
        ladlen = len(self.lad)
        idx = 0
        lastnw = 0
        while idx < ladlen:
            cmnd = self.lad[idx]

            if cmnd == 'NW:':
                # new circuit
                idx += 1
                cmnd = self.lad[idx]
                lastnw += 1
                if lastnw != cmnd:
                    print('Network Number Parse Error!!')
                    sys.exit()
                state = True    # 出力値
                mem = True      # 中間値

            elif cmnd == 'LD' or cmnd == 'LDN':
                idx += 1
                ope = self.lad[idx]
                if cmnd == 'LD':
                    mem = self.memmng.getMemory(ope)
                else:
                    mem = not self.memmng.getMemory(ope)

            elif cmnd == 'AND' or cmnd == 'ANDN':
                state &= mem
            
                idx += 1
                ope = self.lad[idx]
                if cmnd == 'AND':
                    mem = self.memmng.getMemory(ope)
                else:
                    mem = not self.memmng.getMemory(ope)

            elif cmnd == 'OR' or cmnd == 'ORN':
                idx += 1
                ope = self.lad[idx]
                if cmnd == 'OR':
                    mem = mem | self.memmng.getMemory(ope)
                else:
                    mem = mem | (not self.memmng.getMemory(ope))

            elif cmnd == 'OUT':
                state &= mem
            
                idx += 1
                ope = self.lad[idx]
                self.memmng.setMemory(ope, state)

            idx += 1

    # 
    def sleep(self):
        strI = ''
        strO = ''
        strM = ''
        for idx in range(10):
            key = memmng.getInputKey(idx)
            strI += key + ':' + str(self.memmng.getMemory(key)) + ',\t'
            key = memmng.getOutputKey(idx)
            strO += key + ':' + str(self.memmng.getMemory(key)) + ',\t'
            key = memmng.getMemoryKey(idx)
            strM += key + ':' + str(self.memmng.getMemory(key)) + ',\t'
        info = {'timeelapsed': self.ctc.gettimeelapsed()}
        info['strI'] = strI
        info['strO'] = strO
        info['strM'] = strM
        self.procinfo.write(info)

        self.ctc.sleep()


"""cjeck command line options"""
args = sys.argv
if len(args) > 1 and args[1] == '-v':
    print(getVersion())
    sys.exit()

# tnPLC Start
tnplc = tnPLC()
tnplc.start()
