# -*- coding: utf-8 -*-
# module processinfo.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is 'cycle processing infomation logging' for the tnPLC
#
import os

class ProcessInfo:
    """processing infomation log oout"""

    def __init__(self):
        """constructor"""
        self.filename = 'procinfo.log'

    def write(self, info):
        file = open(self.filename, 'w')
        file.write('timeelapsed:' + str(info['timeelapsed']*1000) + ' ms\n')
        file.write('strI:' + info['strI'] + ' \n')
        file.write('strO:' + info['strO'] + ' \n')
        file.write('strM:' + info['strM'] + ' \n')
        file.close()
