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
import ladexecutor
import cycletimectrl
import processinfo


def getVersion():
    """tnPLC Project version"""
    return 'v0.0.5'


class tnPLC:
    """tnPLC main"""

    # constructor
    def __init__(self):
        self.ladparser = ladparser.LADParser()
        # initialize memory manager
        self.memmng = memmng.MemManage()
        self.abtree = None
        # initialize GPIO
        self.gpio = rpgpio.RpGPIO()
        # process inpormation write out
        self.procinfo = processinfo.ProcessInfo()
        self.ladexec = ladexecutor.LADExecutor(self.memmng)

    def start(self):
        """tnPLC startup point"""

        """read argument"""
        args = sys.argv

        """read LAD file"""
        self.abtree = self.ladparser.parseFile(args[1])
        if self.abtree is None:
            print('LAD File[', args[1], '] Parse Errer!')
        else:
            # LAD program start
            print('Start tnPLC')
            self.run()
            print('Finish tnPLC')

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
            pass


    def inputRefuresh(self):
        """refresh GPIO Input"""
        self.memmng.refreshInput(self.gpio)

    def outputRefuresh(self):
        """refresh GPIO Output"""
        self.memmng.refreshOutput(self.gpio)

    def cyclic(self):
        """LAD process"""
        self.ladexec.Execution(self.abtree)
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
arglen=len(args)

if arglen <= 1:
        sys.exit()
if arglen > 1 and args[1] == '-v':
    print(getVersion())
    sys.exit()

# tnPLC Start
tnplc = tnPLC()
tnplc.start()
