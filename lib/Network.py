#!/usr/bin/env python3
# coding: utf8
import Helper


class QCSP(object):
    def __init__(self, algebra, maxIndex, description):
        super(QCSP, self).__init__()
        self.algebra = algebra
        self.nodeCount = maxIndex + 1
        self.description = description
        self.cs = [[self.algebra.Universal
                   for a in range(self.nodeCount)]
                   for b in range(self.nodeCount)]
        self.multiSubsetRelations = []

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

    def enforceOneConsistency(self, symbol):
        bitmask = self.algebra.bitmaskFromList([symbol])
        for i in range(self.nodeCount):
            self.cs[i][i] = bitmask

    def initNontractableRelations(self):
        # init list of nontractable relations
        for i, j in Helper.doubleNested(self.nodeCount):
            setCount = len(self.algebra.aTractableSet(self.cs[i][j]))
            if setCount > 1:
                self.multiSubsetRelations.append([setCount, i, j])

    def listOfNontractableConstraints(self):
        lst = []
        for c, i, j in self.multiSubsetRelations:
            c = len(self.algebra.aTractableSet(self.cs[i][j]))
            if c > 1:
                conn = c
                # for p in range(self.nodeCount):
                #     u = len(self.algebra.aTractableSet(self.cs[i][p]))
                #     v = len(self.algebra.aTractableSet(self.cs[j][p]))
                #     conn = conn + u + v
                lst.append([conn, i, j])
        lst.sort(reverse=True)
        return lst

    def __str__(self):
        relCount = 0
        s = ""
        for a, b in Helper.doubleNested(self.nodeCount):
            if self.cs[a][b] != self.algebra.Universal:
                s += "%d {%s} %d\n" % (
                    a, self.algebra.nameForBitmask(self.cs[a][b]), b)
                relCount += 1
        return "%s (%d nodes, %d relations)\n%s" % (
            self.description, self.nodeCount, relCount, s)
