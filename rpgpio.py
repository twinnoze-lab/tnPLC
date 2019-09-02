# -*- coding: utf-8 -*-
# module rpgpio.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is RaspberyPi GPIO interface for the tnPLC
#

import RPi.GPIO as GPIO  #for the GPIO access libraly

# GPIO Input head pos BCM number
GPIO_INPUT_HEADPOS = 4
GPIO_INPUT_LEN = 12
# GPIO Output head pos BCM number
GPIO_OUTPUT_HEADPOS = 16
GPIO_OUTPUT_LEN = 12

class RpGPIO:
    '''RaspberyPi GPIO Manage'''

    # constructor
    def __init__(self):
        # GPIO access number use by BNC number.
        GPIO.setmode(GPIO.BCM)

        # BCM Number 15-27 use for Output
        for idx in range(0, GPIO_INPUT_LEN):
            GPIO.setup(idx + GPIO_INPUT_HEADPOS, GPIO.IN)

        # BCM Number 2-14 use for Input
        for idx in range(0, GPIO_OUTPUT_LEN):
            GPIO.setup(idx + GPIO_OUTPUT_HEADPOS, GPIO.OUT)

    # GPIO Input Settings
    def getGPIO(self, idx):
        ret = GPIO.input(idx + GPIO_INPUT_HEADPOS)
        if ret == GPIO.HIGH:
            ret = True
        else:
            ret = False
        return ret

    # GPIO Output Settings
    def setGPIO(self, idx, val):
        if val == True:
            GPIO.output(idx + GPIO_OUTPUT_HEADPOS, GPIO.HIGH)
        else:
            GPIO.output(idx + GPIO_OUTPUT_HEADPOS, GPIO.LOW)
    # 
    def finish(self):
        GPIO.cleanup()

