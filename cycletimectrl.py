# -*- coding: utf-8 -*-
# module cycletimectrl.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is cycle time controler for the tnPLC
#
import time

CONSTANT_CYCLE_TIME = 0.100    # 100ms cyclic time


class CycleTimeCtrl:
    """measurement scan time, stabilization"""

    def __init__(self):
        """constructor"""
        self.cycleTime = CONSTANT_CYCLE_TIME
        self.lasttime = time.time()

    def gettimeelapsed(self):
        """time elapsed whth in this cycle"""
        curtime = time.time()
        elapsed = (curtime - self.lasttime)
        return elapsed

    def sleep(self):
        """wait for setting cycle time"""
        waittime = self.cycleTime - self.gettimeelapsed()
        if waittime > 0:
            time.sleep(waittime)
        self.lasttime = time.time()
