# -*- coding: utf-8 -*-
# module ladparser.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is LAD file parser for the tnPLC
#

import pyparsing as pp

class LADParser:
    '''tnPLC LAD File Systax Parse'''

    # constructor
    def __init__(self):
      self.makeLadParser()

    # make LAD parser
    def makeLadParser(self):
      self.NwNumber = pp.Word(pp.nums, max=1).setParseAction(pp.tokenMap(int)).setResultsName('NwNumber')
      self.Nw = pp.Word('NW:').setResultsName('NwID') + self.NwNumber
      self.Mem_I = pp.Combine(pp.Word('I') + pp.Word(pp.nums, max=2)).setResultsName('MemI')
      self.Mem_O = pp.Combine(pp.Word('O') + pp.Word(pp.nums, max=2)).setResultsName('MemO')
      self.Mem = self.Mem_I | self.Mem_O
      self.Command_LD = pp.Word('LD').setResultsName('LD') + self.Mem
      self.Command_OUT = pp.Word('OUT').setResultsName('OUT') + self.Mem
      self.NwProgram = self.Nw + self.Command_LD + self.Command_OUT
      self.Program = pp.OneOrMore(self.NwProgram)

    # check parsed LAD file
    def checkLadParser(self, lad):
        ladlen = len(lad)
        idx = 0
        lastnw = 0
        
        while idx < ladlen:
            line = lad[idx]

            if line == 'NW:':
                # new circuit
                idx += 1
                line = lad[idx]
                lastnw += 1
                if lastnw != line:
                    print('Network Line Parse Error!!')
                    return False
            idx += 1
        return True

    # parse and check input LAD file
    def parseFile(self, filename):
      try:
        lad = self.Program.parseFile(filename, True)
        ret = self.checkLadParser(lad) 
        if ret == False:
            return None
        return lad
      except:
        return None
