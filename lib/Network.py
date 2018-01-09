#!/usr/bin/env python3
# coding: utf8
import Helper


class QCSP(object):
    def __init__(self, algebra, maxIndex, description):
        super(QCSP, self).__init__()
        self.algebra = algebra
        self.nodeCount = maxIndex + 1
        self.description = description
        self.nodeConnectivity = [0] * self.nodeCount
        self.cs = [[self.algebra.Universal
                   for a in range(self.nodeCount)]
                   for b in range(self.nodeCount)]

    def addConstraint(self, A, B, constraint):
        if A >= self.nodeCount or B >= self.nodeCount:
            print("ERROR: Adding Relation to Network (Max Index)")
            return
        constraintMask = self.algebra.bitmaskFromList(constraint)
        converseRelation = self.algebra.converse(constraintMask)
        self.cs[A][B] = constraintMask
        if self.cs[B][A] == self.algebra.Universal:
            self.cs[B][A] = converseRelation
        elif not (self.cs[B][A] & converseRelation):
            print("ERROR: Adding inconsistent constraint:")
            print(" %d->%d  %s  '%s'" % (A, B, constraint, self.description))
            self.cs[A][B] = 0

    def calculateNodeConnectivity(self):
        for (i, j) in Helper.doubleNested(self.nodeCount):
            if self.cs[i][j] != self.algebra.Universal:
                c = bin(self.cs[i][j]).count("1")
                self.nodeConnectivity[i] += c
                self.nodeConnectivity[j] += c

    def enforceOneConsistency(self, symbol):
        bitmask = self.algebra.bitmaskFromList([symbol])
        for i in range(self.nodeCount):
            self.cs[i][i] = bitmask

    def listOfMultiRelationConstraints(self):
        lst = []
        for (i, j) in Helper.doubleNested(self.nodeCount):
            c = bin(self.cs[i][j]).count("1")
            if c > 1 and c < self.algebra.baseCount:  # exclude Universal
                lst.append([i, j])
        return lst

    def listOfNontractableConstraints(self):
        lst = []
        for (i, j) in Helper.doubleNested(self.nodeCount):
            relMask = self.cs[i][j]
            if len(self.algebra.aTractableSet(relMask)) > 1:
                lst.append([i, j])
        return lst

    def __str__(self):
        relCount = 0
        s = ""
        for (a, b) in Helper.doubleNested(self.nodeCount):
            if self.cs[a][b] != self.algebra.Universal:
                s += "%d {%s} %d\n" % (
                    a, self.algebra.nameForBitmask(self.cs[a][b]), b)
                relCount += 1
        return "%s (%d nodes, %d relations)\n%s" % (
            self.description, self.nodeCount, relCount, s)
