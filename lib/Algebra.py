#!/usr/bin/env python
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
            a = self.BaseRelations.index(cv[0])
            b = self.BaseRelations.index(cv[1])
            self.TConverse.setConverseIndex(a, b)
        # Process compositions
        self.TComposition = LookupTable.Composition(self.baseCount)
        for cp in _algebraFile.readComposition():  # format: B1 B2 [B1 B2 B3]
            a = self.BaseRelations.index(cp[0])
            b = self.BaseRelations.index(cp[1])
            c = self.TName.getBitmask(cp[2])
            self.TComposition.setCompositionMask(a, b, c)

    def checkIntegrity(self):
        self.TConverse.checkIntegrity()
        self.TComposition.checkIntegrity()

    def nameForBitmask(self, bitmask):
        return self.TName.getName(bitmask)

    def bitmaskFromList(self, array):
        return self.TName.getBitmask(array)

    def converse(self, rel):
        result = 0
        for x in range(self.baseCount):
            if rel & (1 << x):
                result |= (1 << self.TConverse.converseIndex(x))
        return result

    def compose(self, relA, relB):
        result = 0
        for xA in range(self.baseCount):
            for xB in range(self.baseCount):
                if relA & (1 << xA) and relB & (1 << xB):
                    result |= self.TComposition.compositionMask(xA, xB)
        return result
