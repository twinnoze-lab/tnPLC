# -*- coding: utf-8 -*-
# module ladparser.py
#
# Copyright (c) 2019 T.Tabuchi
#
# this module is LAD file parser for the tnPLC
#
import pyparsing as pp
import abstracttree as at


class LADParser:
    """tnPLC LAD File Systax Parse"""

    def __init__(self):
        """constructor"""
        """make LAD parser"""
        self.NwNumber = pp.Word(pp.nums, max=1).setParseAction(pp.tokenMap(int)).setBreak(False)
        self.Nw = pp.CaselessLiteral('NW:') + self.NwNumber + pp.Suppress(pp.lineEnd())
        self.Ope_I = pp.Combine(pp.CaselessLiteral('I') + pp.Word(pp.nums, max=2))
        self.Ope_O = pp.Combine(pp.CaselessLiteral('O') + pp.Word(pp.nums, max=2))
        self.Ope_M = pp.Combine(pp.CaselessLiteral('M') + pp.Word(pp.nums, max=2))
        self.Ope = self.Ope_I | self.Ope_O | self.Ope_M

        self.Command_LD = (pp.CaselessKeyword('LDN') | pp.CaselessKeyword ('LD')) + self.Ope + pp.Suppress(pp.lineEnd())
        self.Command_AND = (pp.CaselessKeyword('ANDN') | pp.CaselessKeyword ('AND')) + self.Ope + pp.Suppress(pp.lineEnd())
        self.Command_OR = (pp.CaselessKeyword('ORN') | pp.CaselessKeyword('OR')) + self.Ope + pp.Suppress(pp.lineEnd())
        self.Command_OUT = pp.CaselessKeyword('OUT') + self.Ope + pp.Suppress(pp.lineEnd())

        self.Command_BSAND = pp.CaselessKeyword('BSAND') + pp.Suppress(pp.lineEnd())
        self.Command_BFAND = pp.CaselessKeyword('BFAND') + pp.Suppress(pp.lineEnd())
        self.Command_BSOR = pp.CaselessKeyword('BSOR') + pp.Suppress(pp.lineEnd())
        self.Command_BFOR = pp.CaselessKeyword('BFOR') + pp.Suppress(pp.lineEnd())

        self.Command_LDOR = self.Command_LD + self.Command_OR * (0, 7)
        self.Command_ANDOR = self.Command_AND + self.Command_OR * (0, 7)
        self.Command_LDAND  = self.Command_LDOR + self.Command_ANDOR * (0, 7)
        # self.BLOCK_COMPLEX = self.BLOCK + pp.Optional(pp.Or([self.Command_BAND, self.Command_BOR])) + pp.Optional(self.Command_ANDOR)

        self.Complex = pp.Forward()
        self.Block = pp.Group((self.Complex | self.Command_LDAND) + pp.Optional(self.Command_ANDOR * (0, 7)))
        self.ComplexOR = self.Command_BSOR + self.Block + self.Block + self.Command_BFOR
        self.ComplexAND = self.Command_BSAND + self.Block + self.Block + self.Command_BFAND
        self.Complex <<= self.ComplexOR | self.ComplexAND

        self.NwProgram = pp.Group(self.Nw + pp.OneOrMore(self.Block) + self.Command_OUT)

        self.Program = pp.OneOrMore(self.NwProgram)

    def checkLadParser(self, abtree):
        """check parsed LAD file"""
        treelen = len(abtree)
        idx = 0
        lastnw = 0
        
        while idx < treelen:
            ab = abtree[idx]

            lastnw += 1
            if lastnw != ab.number:
                print('Network Line Parse Error!!')
                return False
            idx += 1
        return True

    def parseFile(self, filename):
        """parse and check input LAD file"""
        try:
            lad = self.Program.parseFile(filename, True)

            abtree = at.AbstractTree.makeAbstractTree(lad)
            ret = self.checkLadParser(abtree)
            if ret == False:
                return None
            return abtree
        except pp.ParseException as pe:
            print (pe.line)
            print (' ' * (pe.column - 1) + '^')
            print(pe)
            return None
        except Exception as er:
            print('Get another Parser Exception!')
            # print(er.args)
            # print(sys.exc_info())

            print(type(er))
            print(er.args)
            print(er)
            return None
