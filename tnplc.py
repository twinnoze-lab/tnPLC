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


def getVersion():
    """tnPLC Project version"""
    return 'v0.0.1a'

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

    def start(self):
        """tnPLC startup point"""

        """read argument"""
        args = sys.argv

        """read LAD file"""
        self.lad = self.ladparser.parseFile(args[1])
        if self.lad == None:
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
        if __debug__:
            pass
        else:
            strI = ''
            strO = ''
            for idx in range(10):
                key = memmng.getInputKey(idx)
                strI += key + ':' + str(self.memmng.getInput(key)) + ', '
                key = memmng.getOutputKey(idx)
                strO += key + ':' + str(self.memmng.getOutput(key)) + ', '
            print(strI)
            print(strO)
            print(' ')

    def cyclic(self):
        """LAD process"""
        ladlen = len(self.lad)
        idx = 0
        lastnw = 0
        while idx < ladlen:
            line = self.lad[idx]

            if line == 'NW:':
                # new circuit
                idx += 1
                line = self.lad[idx]
                lastnw += 1
                if lastnw != line:
                    print('Network Line Parse Error!!')
                    sys.exit()
            elif line == 'LD':
                idx += 1
                line = self.lad[idx]
                mem = self.memmng.getMemory(line)
            elif line == 'OUT':
                idx += 1
                line = self.lad[idx]
                self.memmng.setMemory(line, mem)
            idx += 1

    # 
    def sleep(self):
        self.ctc.sleep()


"""cjeck command line options"""
args = sys.argv
if len(args) > 1 and args[1] == '-v':
    print(getVersion())
    sys.exit()

# tnPLC Start
tnplc = tnPLC()
tnplc.start()
