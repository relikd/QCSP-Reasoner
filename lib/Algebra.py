#!/usr/bin/env python
# coding: utf8
import LookupTable


class Algebra(object):
    def __init__(self, _algebraFile):
        super(Algebra, self).__init__()
        self.BaseRelations = _algebraFile.readBaseRelations()
        self.baseCount = len(self.BaseRelations)
        self.TName = LookupTable.Names(self.BaseRelations)
        self.Universal = len(self.TName.labels) - 1
        # Process converses
        self.TConverse = LookupTable.Converse(self.baseCount)
        for cv in _algebraFile.readConverse():
            a = self.TName.getBitmask(cv[0])
            b = self.TName.getBitmask(cv[1])
            self.TConverse.setConverse(a, b)
        # Process compositions
        self.TComposition = LookupTable.Composition(self.baseCount)
        for cp in _algebraFile.readComposition():  # format: B1 B2 [B1 B2 B3]
            a = self.TName.getBitmask(cp[0])
            b = self.TName.getBitmask(cp[1])
            c = self.TName.getBitmask(cp[2])
            self.TComposition.setComposition(a, b, c)

    def checkIntegrity(self):
        self.TConverse.checkIntegrity()
        self.TComposition.checkIntegrity()

    def nameForBitmask(self, bitmask):
        return self.TName.getName(bitmask)

    def bitmaskFromList(self, array):
        return self.TName.getBitmask(array)

    def converse(self, rel):
        return self.TConverse.converse(rel)

    def compose(self, relA, relB):
        return self.TComposition.composition(relA, relB)

    def __str__(self):
        txt = "Name Mapping:\n%s" % str(self.TName)

        txt += "\nTable of Converses:\n"
        for x in self.TConverse.converses:
            txt += "  {:2} : {:2}\n".format(
                self.TName.getName(x),
                self.TName.getName(self.TConverse.converses[x]))

        txt += "\nComposition Table:\n"
        for x in self.TComposition.compositions:
            txt += "  {:2} ⟐ {:2} : {}\n".format(
                self.TName.getName(x[0]),
                self.TName.getName(x[1]),
                self.TName.getName(self.TComposition.compositions[x]))
        return txt
