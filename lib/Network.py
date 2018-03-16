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
        self.stack = [[-99, 0]]
        self.lastModified = [[[0]
                             for a in range(self.nodeCount)]
                             for b in range(self.nodeCount)]
        self.enforceOneConsistency(algebra.equality)

    def updateConstraint(self, A, B, constraint):
        self.stack.append([A, B, self.cs[A][B]])
        self.stack.append([B, A, self.cs[B][A]])
        self.cs[A][B] = constraint
        self.cs[B][A] = self.algebra.converse(constraint)

    def updateOneWay(self, A, B, constraint):
        self.stack.append([A, B, self.cs[A][B]])
        self.cs[A][B] = constraint

    def triangleChanged(self, A, B, K):
        return max(self.lastModified[A][K][-1],
                   self.lastModified[B][K][-1],
                   self.lastModified[A][B][-1])

    def saveBreakpoint(self, A, B, level):
        self.stack.append([-99, level])
        if self.lastModified[A][B][-1] < level:
            self.lastModified[A][B].append(level)
            self.lastModified[B][A].append(level)

    def restoreBreakpoint(self, level):
        while len(self.stack) > 0:  # restore previous state
            itm = self.stack.pop()
            if itm[0] == -99:
                if level == 0 or itm[1] == level:
                    return
                continue
            self.cs[itm[0]][itm[1]] = itm[2]
            if level > 0:
                modifyArr = self.lastModified[itm[0]][itm[1]]
                while modifyArr[-1] > level:
                    modifyArr.pop()

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

    def listOfNontractableConstraints(self):
        lst = []
        for i in range(0, self.nodeCount):
            for j in range(i + 1, self.nodeCount):
                c = len(self.algebra.aTractableSet(self.cs[i][j]))
                if c > 1:
                    conn = (Helper.subsetScore[self.cs[i][j]] + (
                        Helper.subsetScore[self.cs[j][i]])) / c
                    # conn = c * 818  # sum of all scores
                    # for p in range(self.nodeCount):
                    #     conn -= Helper.subsetScore[self.cs[p][i]]
                    #     ...
                    lst.append([conn, c, i, j, self.cs[i][j]])
        lst.sort()
        return lst

    def inPreviousNontractableSet(self, c, i, j, level, oldList):
        lIndex = len(oldList)
        while lIndex:
            lIndex -= 1
            if oldList[lIndex][2] == i and oldList[lIndex][3] == j:
                if c > oldList[lIndex][1]:
                    sIndex = len(self.stack)
                    while sIndex:
                        sIndex -= 1
                        itm = self.stack[sIndex]
                        A = itm[0]
                        B = itm[1]
                        if A == -99:
                            break
                        elif ((A == i and B == j) or
                              (A == j and B == i)):
                            self.cs[A][B] = itm[2]
                            del self.stack[sIndex]
                            if level > 1:
                                modifyArr = self.lastModified[A][B]
                                if modifyArr[-1] == (level - 1):
                                    modifyArr.pop()
                del(oldList[lIndex])
                return True
        return False

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
