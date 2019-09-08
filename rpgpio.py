# -*- coding: utf-8 -*-
# module rpgpio.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is RaspberyPi GPIO interface for the tnPLC
#
import importlib

# GPIO Input head pos BCM number
GPIO_INPUT_HEADPOS = 4
GPIO_INPUT_LEN = 12
# GPIO Output head pos BCM number
GPIO_OUTPUT_HEADPOS = 16
GPIO_OUTPUT_LEN = 12


class RpGPIO:
    """RaspberyPi GPIO Manage"""

    def __init__(self):
        """constructor"""
        if __debug__:
            #import RPi.GPIO as GPIO  # for the GPIO access libraly
            self.gpio = importlib.import_module('RPi.GPIO')
            # GPIO access number use by BNC number.
            self.gpio.setmode(self.gpio.BCM)

            # BCM Number 15-27 use for Output
            for idx in range(0, GPIO_INPUT_LEN):
                self.gpio.setup(idx + GPIO_INPUT_HEADPOS, self.gpio.IN)

            # BCM Number 2-14 use for Input
            for idx in range(0, GPIO_OUTPUT_LEN):
                self.gpio.setup(idx + GPIO_OUTPUT_HEADPOS, self.gpio.OUT)
        else:
            self.debugGPIO_I = [False, False, False, False, False, False, False, False, False, False, False, False]
            self.debugGPIO_O = [False, False, False, False, False, False, False, False, False, False, False, False]

    def getGPIO(self, idx):
        """GPIO Input Settings"""
        if __debug__:
            ret = self.gpio.input(idx + GPIO_INPUT_HEADPOS)
            if ret == self.gpio.HIGH:
                ret = True
            else:
                ret = False
        else:
            ret = self.debugGPIO_I[idx]
        return ret

    def setGPIO(self, idx, val):
        """GPIO Output Settings"""
        if __debug__:
            if val == True:
                self.gpio.output(idx + GPIO_OUTPUT_HEADPOS, self.gpio.HIGH)
            else:
                self.gpio.output(idx + GPIO_OUTPUT_HEADPOS, self.gpio.LOW)
        else:
            self.debugGPIO_O[idx]=val

    def finish(self):
        """clear the GPIO setting"""
        if __debug__:
            self.gpio.cleanup()

