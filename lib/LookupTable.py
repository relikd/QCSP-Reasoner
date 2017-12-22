#!/usr/bin/env python
# coding: utf8
import Helper


class Conve(object):
    def __init__(self, numberOfBaseRelations):
        super(Conve, self).__init__()
        self.baseCount = numberOfBaseRelations
        self.converses = [None] * (1 << self.baseCount)

    def setConverse(self, a, b):
        self.converses[a] = b
        # self.converses[b] = a

    def converse(self, i):
        return self.converses[i]

    def checkIntegrity(self):
        print "Checking Converse Integrity ..."
        for i in range(self.baseCount):
            if self.converses[1 << i] is None:  # Only base relations
                print "Couldn't find converse for '{:0{}b}'"\
                    .format(1 << i, self.baseCount)


class Compo(object):
    def __init__(self, numberOfBaseRelations):
        super(Compo, self).__init__()
        self.baseCount = numberOfBaseRelations
        self.compositions = [[None] * self.baseCount] * self.baseCount

    def setComposition(self, s1, s2, composition):
        self.compositions[s1][s2] = composition

    def composition(self, s1, s2):
        return self.compositions[s1][s2]

    def checkIntegrity(self):
        print "Checking Composition Integrity ..."
        n = self.baseCount
        for (x, y) in [(i / n, i % n) for i in range(n**2)]:
            if self.compositions[x][y] is None:
                print "Couldn't find composition for '{0:0{2}b} * {1:0{2}b}'"\
                    .format(1 << x, 1 << y, self.baseCount)


class Nam(object):
    def __init__(self, symbols):
        super(Nam, self).__init__()
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


class Composition(object):
    def __init__(self, *symbols):
        super(Composition, self).__init__()
        self.baseRelations = frozenset(symbols)
        self.compositions = dict()
        self.converses = dict()

    def addConverse(self, symbol, converse, BiDirectional=False):
        self.converses[symbol] = converse
        if BiDirectional:
            self.converses[converse] = symbol

    def converse(self, symbol):
        return self.converses[symbol]

    def addComposition(self, s1, s2, composition, OrderIrrelevant=False):
        self.compositions[s1, s2] = frozenset(composition)
        if OrderIrrelevant:
            self.compositions[s2, s1] = frozenset(composition)

    def composition(self, symbol):
        return self.compositions[symbol]

    def setEquiCompositions(self):
        for s in self.baseRelations:
            self.compositions[s, s] = frozenset(s)

    def checkIntegrity(self):
        print "Checking Integrity ..."
        for sym_a in self.baseRelations:
            try:
                self.converses[sym_a]
            except KeyError:
                print("Couldn't find converse for symbol '%s'" % sym_a)
            for sym_b in self.baseRelations:
                try:
                    self.compositions[sym_a, sym_b]
                except KeyError:
                    print("Couldn't find compositions for {'%s','%s'}" %
                          (sym_a, sym_b))


class Names(object):
    def __init__(self, *symbols):
        super(Names, self).__init__()
        self.baseRelations = frozenset(symbols)
        self.labels = dict()
        self.labels[frozenset([])] = "Empty Set"
        self.labels[self.baseRelations] = "Universe"

    def set(self, name, *symbol):
        self.labels[frozenset(symbol)] = name

    def get(self, symbol):
        return self.labels[symbol]

    def print_JEPD_set(self):
        for x in Helper.powerset(list(self.baseRelations)):
            theSet = frozenset(x)
            txt = "  {%s}" % (','.join(x))
            try:
                txt += " \t\t(%s)" % (self.get(theSet))
            except KeyError:
                pass
            print(txt)


# Point Calculus
# L = Composition("<", ">", "=")
# L.addConverse("=", "=")
# L.addConverse("<", ">", True)  # True means bidirectional converse
# L.setEquiCompositions()  # set << = <  AND  >> = >  AND == = =
# L.addComposition("<", "=", "<", True)  # True means order doesn't matter
# L.addComposition(">", "=", ">", True)
# L.addComposition("<", ">", ["<", ">", "="], True)
# L.checkIntegrity()
