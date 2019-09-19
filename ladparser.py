# -*- coding: utf-8 -*-
# module ladparser.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is LAD file parser for the tnPLC
#
import pyparsing as pp


class LADParser:
    """tnPLC LAD File Systax Parse"""

    def __init__(self):
        """constructor"""
        self.makeLadParser()

    def makeLadParser(self):
        """make LAD parser"""
        self.NwNumber = pp.Word(pp.nums, max=1).setParseAction(pp.tokenMap(int))
        self.Nw = pp.Literal('NW:') + self.NwNumber
        self.Ope_I = pp.Combine(pp.Literal('I') + pp.Word(pp.nums, max=2))
        self.Ope_O = pp.Combine(pp.Literal('O') + pp.Word(pp.nums, max=2))
        self.Ope_M = pp.Combine(pp.Literal('M') + pp.Word(pp.nums, max=2))
        self.Ope = self.Ope_I | self.Ope_O | self.Ope_M
        self.Command_LD = (pp.Literal('LDN') | pp.Literal('LD')) + self.Ope
        self.Command_AND = (pp.Literal('ANDN') | pp.Literal('AND')) + self.Ope
        self.Command_OR = (pp.Literal('ORN') | pp.Literal('OR')) + self.Ope
        self.Command_OUT = pp.Literal('OUT') + self.Ope
        self.Command_LDOR = self.Command_LD +  self.Command_OR*(0, 7)
        self.Command_ANDOR = self.Command_AND +  self.Command_OR*(0, 7)
        self.NwProgram = self.Nw + self.Command_LDOR + self.Command_ANDOR*(0, 7) + self.Command_OUT
        self.Program = pp.OneOrMore(self.NwProgram)

    def checkLadParser(self, lad):
        """check parsed LAD file"""
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

    def parseFile(self, filename):
        """parse and check input LAD file"""
        try:
            lad = self.Program.parseFile(filename, True)
            ret = self.checkLadParser(lad)
            if ret == False:
                return None
            return lad
        except:
            return None
