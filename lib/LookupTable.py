#!/usr/bin/env python
# coding: utf8
import Helper


class Converse(object):
    def __init__(self, numberOfBaseRelations):
        super(Converse, self).__init__()
        self.baseCount = numberOfBaseRelations
        self.converse = [0 for x in range(1 << self.baseCount)]

    def precalc(self):
        for x in range(1, 1 << self.baseCount):
            result = 0
            for baseRel in Helper.bits(x):
                result |= self.converse[baseRel]
            self.converse[x] = result

    def checkIntegrity(self):
        print("Checking Converse Integrity ...")
        for i in range(self.baseCount):
            if self.converse[1 << i] is None:  # Only base relations
                print("Couldn't find converse for '{:0{}b}'"
                      .format(1 << i, self.baseCount))


class Composition(object):
    def __init__(self, numberOfBaseRelations):
        super(Composition, self).__init__()
        self.baseCount = numberOfBaseRelations
        self.compositions = dict()

    def setComposition(self, a, b, compositionMask):
        index = (a << self.baseCount) + b
        self.compositions[index] = compositionMask

    def composition(self, a, b):
        # try:
        index = (a << self.baseCount) + b
        return self.compositions[index]
        # except KeyError:
        #     result = 0
        #     for baseRelA in Helper.bits(a):
        #         for baseRelB in Helper.bits(b):
        #             index = (baseRelA << self.baseCount) + baseRelB
        #             result |= self.compositions[index]
        #     self.setComposition(a, b, result)
        #     return result

    def checkIntegrity(self):
        print("Checking Composition Integrity ...")
        n = self.baseCount
        for x, y in [(i / n, i % n) for i in range(n**2)]:
            index = ((1 << x) << self.baseCount) + (1 << y)
            if self.compositions[index] is None:
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
                    self.labels[i] += " %s" % symbols[x]
            self.labels[i] = self.labels[i][1:]

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


class ATractable(object):
    def __init__(self, stopAfter):
        super(ATractable, self).__init__()
        self.subsets = dict()
        self.subsets[0] = [0]
        self.defineCounter = 1
        self.defineTreshhold = int(stopAfter)

    def setClosedSet(self, s, subset):
        # try:
        #     self.subsets[s]
        #     print("ERROR: Key already exist. Should never be overwritten.")
        # except KeyError:
        # subset.reverse()
        self.subsets[s] = subset
        self.defineCounter += 1

    def getClosedSet(self, s):
        # try:
        return self.subsets[s]
        # except KeyError:
        #     arr = self.fastNonOptimalSubset(s)
        #     self.setClosedSet(s, arr)
        #     # print("WARN: Key doesn't exist. Calculating on the fly.\n%s" % arr)
        #     return arr

    def fastNonOptimalSubset(self, s):
        arr = []
        prev = 0
        for a in Helper.bits(s):
            try:
                self.subsets[prev | a]
                prev |= a
                continue
            except KeyError:
                arr += [prev]
                prev = a  # reset
        return arr + [prev]

    def partitionScore(self, partitionSet):
        totalScore = 0
        setSize = len(partitionSet)
        for x in partitionSet:
            partScore = Helper.subsetScore[x]
            bits = Helper.countBits[x]
            # A: AVG subset score
            # totalScore += partScore / float(max(1, bits))
            # B: Entropy: prefer fewer, equal sized subsets
            # totalScore += setSize**bits
            # C: Score weighted Entropy
            totalScore += setSize**bits / float(max(1, partScore))
            # D: Asymetric: prefer fewer subsets but create large groups
            # totalScore += setSize / float(max(bits, 1))
            # E: Score weighted Asymetric
            # totalScore += setSize / float(max(partScore, 1))
        return totalScore

    def calculateCombinations(self, maxSetSize=2):
        print("%d combinations:" % maxSetSize)
        a = int(maxSetSize / 2)
        b = maxSetSize - a
        while a >= 1:  # try all combinations eg. for 6: 3+3, 2+4, 1+5
            firstSet = [x for x in self.subsets if len(self.subsets[x]) == a]
            secondSet = [y for y in self.subsets if len(self.subsets[y]) == b]
            a -= 1
            b += 1
            for x in firstSet:
                for y in secondSet:
                    cmb = self.subsets[x] + self.subsets[y]
                    try:
                        score = self.partitionScore(cmb)
                        preScore = self.partitionScore(self.subsets[x | y])
                        if score < preScore:
                            self.subsets[x | y] = cmb
                        continue  # skip already existing
                    except KeyError:
                        pass
                    # construct new array with both array subsets
                    self.subsets[x | y] = cmb
                    self.defineCounter += 1
            print("Defined combinations %d" % self.defineCounter)
            if self.defineCounter >= self.defineTreshhold:
                return
        self.calculateCombinations(maxSetSize + 1)  # recursive call
