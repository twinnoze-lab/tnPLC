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

class tnPLC:
    '''tnPLC main'''

    # constructor
    def __init__(self):
        self.ladparser = ladparser.LADParser()
        # initialize memory manager
        self.memmng = memmng.MemManage()
        self.lad = 0
        # initialize GPIO
        self.gpio = rpgpio.RpGPIO()

    # tnPLC startup point 
    def start(self):
        # read argument
        args = sys.argv

        # read LAD file 
        self.lad = self.ladparser.parseFile(args[1])
        if self.lad == None:
            print('LAD File[', args[1], '] Parse Errer!')
        else:
            # LAD program start
            self.run()

        # cleanup GPIO
        self.gpio.finish()
        return

    # cyclic RUN
    def run(self):
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
          

    # refresh GPIO Input
    def inputRefuresh(self):
        self.memmng.refreshInput(self.gpio)

    # refresh GPIO Output
    def outputRefuresh(self):
        self.memmng.refreshOutput(self.gpio)

    # LAD process
    def cyclic(self):
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
                mem = self.memmng.getInput(line)
            elif line == 'O':
                idx += 1
                line = self.lad[idx]
                self.memmng.setOutput(line, mem)
            idx += 1

    # 
    def sleep(self):
        self.ctc.sleep()

# tnPLC Start
tnplc = tnPLC()
tnplc.start()
