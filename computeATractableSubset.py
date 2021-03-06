#!/usr/bin/env python
# coding: utf8
from lib import LookupTable, ReadFile, Helper

algFile = ReadFile.AlgebraFile("algebra/allen.txt")
BaseRelations = algFile.readBaseRelations()
TName = LookupTable.Names(BaseRelations)

aTractableFile = ReadFile.ATractableSubsetsFile("algebra/ia_ord_horn.txt")

# Process a-tractable subsets for improved refinement search
theTable = LookupTable.ATractable(round((1 << len(BaseRelations)) * 0.99))
print("Calculating A-Tractable subclasses ...")
for (index, subsets) in aTractableFile.readSubset(TName):
    theTable.setClosedSet(index, subsets)

print("%d" % len(theTable.subsets))
theTable.calculateCombinations()
print("%d of %d\n" % (len(theTable.subsets), 2**13))


def printUpdatedTractableSet():
    for key in theTable.subsets:
        txt = ""
        tmpOrdered = []
        for subset in theTable.subsets[key]:
            subsetScore = Helper.subsetScore[subset]  # bin(subset).count("1")
            tmpOrdered += [(subsetScore, subset)]
        tmpOrdered.sort()
        for (x, subset) in tmpOrdered:
            txt += "%s | " % TName.getName(subset)
        print txt[:-3]


printUpdatedTractableSet()
