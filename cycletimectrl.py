# -*- coding: utf-8 -*-
# module cycletimectrl.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is cycle time controler for the tnPLC
#

import time
from time import sleep

CONSTANT_CYCLE_TIME = 0.100    # 100ms cyclic time

class CycleTimeCtrl:
    '''measurement scan time, stabilization'''

    # constructor
    def __init__(self):
        self.cycleTime = CONSTANT_CYCLE_TIME
        self.lasttime = time.time()

    # wait for setting cycle time
    def sleep(self):
        curtime = time.time()
        waittime = self.cycleTime - (curtime - self.lasttime)
        if waittime>0:
            time.sleep(waittime)

        self.lasttime = time.time()

