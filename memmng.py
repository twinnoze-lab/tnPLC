# -*- coding: utf-8 -*-
# module memmng.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is Memory Manager for the tnPLC
#
import rpgpio


def getInputKey(idx):
    """Create a I[nn] Key"""
    key = 'I' + str(idx).zfill(2)
    return key


def getOutputKey(idx):
    """Create a O[nn] Key"""
    key = 'O' + str(idx).zfill(2)
    return key


class MemManage:
    """tnPLC I/O Data"""

    def __init__(self):
        """constructor"""
        self.Input = {}
        self.Output = {}
        for idx in range(0, rpgpio.GPIO_INPUT_LEN):
            key = getInputKey(idx)
            self.Input.update({key: False})
            key = getOutputKey(idx)
            self.Output.update({key: False})

    def getInput(self, inp):
        """return I[nn] data"""
        return self.Input[inp]

    def setInput(self, inp, val):
        """setting up I[nn] data by val data"""
        ret = self.Input.update({inp: val})
        return ret

    def getOutput(self, outp):
        """return O[nn] data"""
        return self.Output[outp]

    def setOutput(self, outp, val):
        """setting up O[nn] data by val data"""
        ret = self.Output.update({outp: val})
        return ret

    def getMemory(self, mem):
        """return Memory data"""
        if mem[0] == 'I':
            ret = self.Input[mem]
        elif mem[0] == 'O':
            ret = self.Output[mem]
        else:
            pass
        return ret

    def setMemory(self, mem, val):
        """setting up Memory data by val data"""
        if mem[0] == 'I':
            ret = self.Input.update({mem: val})
        elif mem[0] == 'O':
            ret = self.Output.update({mem: val})
        else:
            pass
        return ret

    def refreshInput(self, gpio):
        """refresh I[nn] data by gpio raw data"""
        for idx in range(0, rpgpio.GPIO_INPUT_LEN):
            key = getInputKey(idx)
            val = gpio.getGPIO(idx)
            self.Input.update({key: val})

    def refreshOutput(self, gpio):
        """refresh gpio raw data by I[nn] data"""
        for idx in range(0, rpgpio.GPIO_OUTPUT_LEN):
            key = getOutputKey(idx)
            mem = self.getOutput(key)
            gpio.setGPIO(idx, mem)

