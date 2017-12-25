#!/usr/bin/env python
# coding: utf8
import Helper


class Converse(object):
    def __init__(self, numberOfBaseRelations):
        super(Converse, self).__init__()
        self.baseCount = numberOfBaseRelations
        self.converses = dict()

    def setConverse(self, a, b):
        self.converses[a] = b

    def converse(self, a):
        try:
            return self.converses[a]
        except KeyError:
            result = 0
            for baseRel in Helper.bits(a):
                result |= self.converses[baseRel]
            self.setConverse(a, result)
            return result

    def checkIntegrity(self):
        print("Checking Converse Integrity ...")
        for i in range(self.baseCount):
            if self.converses[1 << i] is None:  # Only base relations
                print("Couldn't find converse for '{:0{}b}'"
                      .format(1 << i, self.baseCount))


class Composition(object):
    def __init__(self, numberOfBaseRelations):
        super(Composition, self).__init__()
        self.baseCount = numberOfBaseRelations
        self.compositions = dict()

    def setComposition(self, a, b, compositionMask):
        self.compositions[a, b] = compositionMask

    def composition(self, a, b):
        try:
            return self.compositions[a, b]
        except KeyError:
            result = 0
            for baseRelA in Helper.bits(a):
                for baseRelB in Helper.bits(b):
                    result |= self.compositions[baseRelA, baseRelB]
            self.setComposition(a, b, result)
            return result

    def checkIntegrity(self):
        print("Checking Composition Integrity ...")
        n = self.baseCount
        for (x, y) in [(i / n, i % n) for i in range(n**2)]:
            if self.compositions[1 << x, 1 << y] is None:
                print("Couldn't find composition for '{0:0{2}b} * {1:0{2}b}'"
                      .format(1 << x, 1 << y, self.baseCount))


class Names(object):
    def __init__(self, symbols):
        super(Names, self).__init__()
        self.baseCount = len(symbols)
        self.labels = [""] * (1 << self.baseCount)
        self.labels[0] = "ø"  # "Empty Set"
        self.labels[-1] = "U"  # "Universe"
        for i in range(1, len(self.labels) - 1):  # base relations
            for x in range(self.baseCount):
                if i & (1 << x):
                    self.labels[i] += ",%s" % symbols[x]
            self.labels[i] = self.labels[i][1:]

    def setName(self, i, name):
        self.labels[i] = name

    def getName(self, i):
        return self.labels[i]

    def getBitmask(self, symbols):
        if not isinstance(symbols, list):
            symbols = [symbols]
        mask = 0
        for i in range(self.baseCount):
            if self.labels[1 << i] in symbols:
                mask |= 1 << i
        return mask

    def __str__(self):
        s = ""
        for i in range(len(self.labels)):
            s += "{:0{}b}  {}\n".format(i, self.baseCount, self.labels[i])
        return s
