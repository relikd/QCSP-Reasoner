#!/usr/bin/env python
# coding: utf8
import LookupTable
import ReadFile

baseCount = 0


def PC():
    algFile = ReadFile.AlgebraFile("algebra/point_calculus.txt")
    alg = Algebra(algFile)
    alg.equality = "="
    return alg


def Allen(fileUsesMathSigns=True):
    if fileUsesMathSigns:
        file1 = "algebra/allen2.txt"
        file2 = "algebra/ia_ord_horn_C2.txt"
    else:
        file1 = "algebra/allen.txt"
        file2 = "algebra/ia_ord_horn_C.txt"

    algFile = ReadFile.AlgebraFile(file1)
    horn = ReadFile.ATractableSubsetsFile(file2)
    alg = Algebra(algFile, horn)
    alg.equality = ("=" if fileUsesMathSigns else "EQ")
    # print(alg)
    alg.checkIntegrity()
    print("Reading compositions file ...")
    print("\n")
    alg.readCompositionsFile("algebra/allen.compositions")
    return alg


class Algebra(object):
    def __init__(self, _algebraFile, _aTractableSubsetsFile=None):
        super(Algebra, self).__init__()
        self.BaseRelations = _algebraFile.readBaseRelations()
        global baseCount
        baseCount = len(self.BaseRelations)
        self.TName = LookupTable.Names(self.BaseRelations)
        self.Universal = len(self.TName.labels) - 1
        self.equality = "EQ"
        self.compose = [[8191
                        for a in range(1 << baseCount)]
                        for b in range(1 << baseCount)]
        # Process converses
        self.TConverse = LookupTable.Converse(baseCount)
        for cv in _algebraFile.readConverse():
            a = self.TName.getBitmask(cv[0])
            b = self.TName.getBitmask(cv[1])
            self.TConverse.converse[a] = b
        self.TConverse.precalc()
        # Process compositions
        # self.TComposition = LookupTable.Composition(baseCount)
        # for cp in _algebraFile.readComposition():  # format: B1 B2 [B1 B2 B3]
        #     a = self.TName.getBitmask(cp[0])
        #     b = self.TName.getBitmask(cp[1])
        #     c = self.TName.getBitmask(cp[2])
        #     self.TComposition.setComposition(a, b, c)
        # Process a-tractable subsets for improved refinement search
        self.TTractable = LookupTable.ATractable(baseCount)
        if _aTractableSubsetsFile is not None:
            for i, subsets in _aTractableSubsetsFile.readSubset(self.TName):
                self.TTractable.setClosedSet(i, subsets)

    def readCompositionsFile(self, filename):
        f = open(filename, "rb")
        temporary = bytearray(f.read())
        f.close()
        for x in range(0, len(temporary), 6):
            relA = (temporary[x + 0] << 8) + (temporary[x + 1] & 255)
            relB = (temporary[x + 2] << 8) + (temporary[x + 3] & 255)
            comp = (temporary[x + 4] << 8) + (temporary[x + 5] & 255)
            self.compose[relA][relB] = comp

    def checkIntegrity(self):
        self.TConverse.checkIntegrity()
        # self.TComposition.checkIntegrity()

    def nameForBitmask(self, bitmask):
        return self.TName.getName(bitmask)

    def bitmaskFromList(self, array):
        return self.TName.getBitmask(array)

    def converse(self, rel):
        return self.TConverse.converse[rel]

    def aTractableSet(self, rel):
        return self.TTractable.getClosedSet(rel)

    def __str__(self):
        txt = "Name Mapping:\n%s" % str(self.TName)

        txt += "\nTable of Converses:\n"
        for x in self.TConverse.converses:
            txt += "  {:2} : {:2}\n".format(
                self.TName.getName(x),
                self.TName.getName(self.TConverse.converse[x]))

        txt += "\nComposition Table:\n"
        for x in self.TComposition.compositions:
            txt += "  {:2} ⟐ {:2} : {}\n".format(
                self.TName.getName(x >> baseCount),
                self.TName.getName(x & ((1 << baseCount) - 1)),
                self.TName.getName(self.TComposition.compositions[x]))
        return txt
