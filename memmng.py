# -*- coding: utf-8 -*-
# module memmng.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is Memory Manager for the tnPLC
#

import rpgpio

# Create a I[nn] Key
def getInputKey(idx):
    key = 'I' + str(idx).zfill(2)
    return key

# Create a O[nn] Key
def getOutputKey(idx):
    key = 'O' + str(idx).zfill(2)
    return key

class MemManage:
    '''tnPLC I/O Data'''

    # constructor
    def __init__(self):
        self.Input = {}
        self.Output = {}
        for idx in range(0, rpgpio.GPIO_INPUT_LEN):
            key = getInputKey(idx)
            self.Input.update({key: False})
            key = getOutputKey(idx)
            self.Output.update({key: False})

    # return I[nn] data
    def getInput(self, inp):
        return self.Input[inp]

    # setting up I[nn] data by val data
    def setInput(self, inp, val):
        ret = self.Input.update({inp: val})
        return ret

    # return O[nn] data
    def getOutput(self, outp):
        return self.Output[outp]

    # setting up O[nn] data by val data
    def setOutput(self, outp, val):
        ret = self.Output.update({outp: val})
        return ret

    # refresh I[nn] data by gpio raw data
    def refreshInput(self, gpio):
        for idx in range(0, rpgpio.GPIO_INPUT_LEN):
            key = getInputKey(idx)
            val = gpio.getGPIO(idx)
            self.Input.update({key: val})

    # refresh gpio raw data by I[nn] data
    def refreshOutput(self, gpio):
        for idx in range(0, rpgpio.GPIO_OUTPUT_LEN):
            key = getOutputKey(idx)
            mem = self.getOutput(key)
            gpio.setGPIO(idx, mem)

