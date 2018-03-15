#!/usr/bin/env python3
# coding: utf8
from lib import Algebra, ReadFile, Helper, Network, Queue
import timeit
import copy

CONSISTENT = "CONSISTENT"
INCONSISTENT = "INCONSISTENT"
refinementCounter = 0
backjumpLevel = 0


class Search(object):
    def __init__(self, network):
        super(Search, self).__init__()
        self.net = network
        self.markTried = set([])
        self.triedStack = []

    def aClosureV1(self):
        s = True
        while s:
            s = False
            for i, j, k in Helper.tripleNested(self.net.nodeCount):
                Cij = self.net.cs[i][j]
                Cjk = self.net.cs[j][k]
                Cik = self.net.cs[i][k]
                # if Cij != self.net.algebra.Universal and\
                #    Cjk != self.net.algebra.Universal:
                Cik_star = Cik & self.net.algebra.compose(Cij, Cjk)
                if Cik != Cik_star:
                    self.net.cs[i][k] = Cik_star
                    s = True
                if Cik_star == 0:
                    return INCONSISTENT  # early exit
        return CONSISTENT

    def aClosureV2(self, arcs=None):
        q = Queue.QQueue()
        if arcs is None:
            for i, j in Helper.doubleNested(self.net.nodeCount):
                q.enqueue(i, j, self.net.cs[i][j])
        else:
            for arc in arcs:
                q.enqueue(arc[0], arc[1], self.net.cs[arc[0]][arc[1]])

        while not q.isEmpty():
            i, j = q.dequeue()
            for k in range(self.net.nodeCount):
                if k == i or k == j:
                    continue
                Cij = self.net.cs[i][j]
                Cjk = self.net.cs[j][k]
                Cik = self.net.cs[i][k]
                Cik_star = Cik & self.net.algebra.compose(Cij, Cjk)
                if Cik_star != Cik:
                    self.net.cs[i][k] = Cik_star
                    q.enqueueNew(i, k, Cik_star)
                    self.net.cs[k][i] &= self.net.algebra.converse(Cik_star)
                    q.enqueueNew(k, i, self.net.cs[k][i])
                Ckj = self.net.cs[k][j]
                Cki = self.net.cs[k][i]
                Ckj_star = Ckj & self.net.algebra.compose(Cki, Cij)
                if Ckj_star != Ckj:
                    self.net.cs[k][j] = Ckj_star
                    q.enqueueNew(k, j, Ckj_star)
                    self.net.cs[j][k] &= self.net.algebra.converse(Ckj_star)
                    q.enqueueNew(j, k, self.net.cs[j][k])
                if Cik_star == 0 or Ckj_star == 0:
                    return INCONSISTENT  # early exit
        return CONSISTENT

    def refinementV15(self, E=None):
        global refinementCounter
        refinementCounter += 1
        # print ".",
        C_star = copy.copy(self.net)
        C_star.cs = copy.deepcopy(self.net.cs)

        aClosed = Search(C_star).aClosureV2(E)
        if aClosed is INCONSISTENT:
            return INCONSISTENT

        refineList = C_star.listOfNontractableConstraints()
        if len(refineList) == 0:  # all rel's have 1 base relation
            if Search(C_star).aClosureV2() == CONSISTENT:
                # print("Resulting QCSP:\n%s" % C_star)
                return CONSISTENT

        for c, i, j in refineList:
            prevRel = C_star.cs[i][j]
            # for baseRel in self.net.algebra.aTractableSet(prevRel):
            for baseRel in Helper.bits(prevRel):
                C_star.cs[i][j] = baseRel
                if Search(C_star).refinementV15([[i, j]]) == CONSISTENT:
                    return CONSISTENT
            C_star.cs[i][j] = prevRel
        return INCONSISTENT

    def aClosureV3(self, arcs):
        global backjumpLevel
        q = Queue.QQueue()
        # if arcs is None:
        #     for i in range(0, self.net.nodeCount):
        #         for j in range(i + 1, self.net.nodeCount):
        #             rel = self.net.cs[i][j]
        #             if rel != self.net.algebra.Universal:
        #                 q.enqueue(i, j, rel)
        # else:
        for arc in arcs:
            q.enqueue(arc[0], arc[1], self.net.cs[arc[0]][arc[1]])

        while q.pq:
            i, j = q.dequeue()
            for k in range(self.net.nodeCount):
                if k == i or k == j:
                    continue
                Cij = self.net.cs[i][j]
                Cjk = self.net.cs[j][k]
                Cik = self.net.cs[i][k]
                Ckj = self.net.cs[k][j]
                Cki = self.net.cs[k][i]
                Cik_star = Cik & self.net.algebra.compose(Cij, Cjk)
                Ckj_star = Ckj & self.net.algebra.compose(Cki, Cij)
                if Cik_star == 0 or Ckj_star == 0:
                    backjumpLevel = self.net.triangleChanged(i, j, k)
                    return INCONSISTENT  # early exit
                if Cik_star != Cik:
                    self.net.updateConstraint(i, k, Cik_star)
                    q.enqueue(i, k, Cik_star)
                if Ckj_star != Ckj:
                    self.net.updateConstraint(k, j, Ckj_star)
                    q.enqueue(k, j, Ckj_star)
        return CONSISTENT

    def refinementV2(self, E=None, listNC=[]):
        global refinementCounter, backjumpLevel
        refinementCounter += 1
        currentLevel = refinementCounter
        # print ".",

        aClosed = self.aClosureV3(E)
        if aClosed is INCONSISTENT:
            return INCONSISTENT

        refineList = self.net.listOfNontractableConstraints()
        if len(refineList) == 0:  # all rel's have 1 base relation
            return CONSISTENT

        for con, c, i, j, prevRel in refineList:
            # for con2, c2, i2, j2, prevRel2 in listNC:
            #     if i == i2 and j == j2 and c > c2:
            #         for x in range(len(self.net.stack) - 1, 0, -1):
            #             itm = self.net.stack[x]
            #             if itm[0] == -99:
            #                 break
            #             elif ((itm[0] == i and itm[1] == j) or
            #                   (itm[0] == j and itm[1] == i)):
            #                 self.net.cs[itm[0]][itm[1]] = itm[2]
            #                 del self.net.stack[x]
            #                 if (currentLevel > 1 and
            #                     self.net.lastModified[itm[0]][itm[1]][-1] == (
            #                         currentLevel - 1)):
            #                     self.net.lastModified[itm[0]][itm[1]].pop()
            # prevRel = self.net.cs[i][j]
            # for baseRel in Helper.bits(prevRel):
            for baseRel in self.net.algebra.aTractableSet(prevRel):
                self.net.saveBreakpoint(i, j, currentLevel)
                self.net.updateConstraint(i, j, baseRel)
                # self.net.updateOneWay(i, j, baseRel)

                if self.refinementV2([[i, j]], refineList) == CONSISTENT:
                    return CONSISTENT

                if currentLevel > backjumpLevel and backjumpLevel > 0:
                    return INCONSISTENT

                self.net.restoreBreakpoint(backjumpLevel)
        return INCONSISTENT

    def refinementV3(self, E=None, listNC=[]):
        global refinementCounter, backjumpLevel

        aClosed = self.aClosureV3()
        if aClosed is INCONSISTENT:
            return INCONSISTENT

        def Select(refineList):
            for con, c, i, j, prevRel in refineList:
                for r in self.net.algebra.aTractableSet(prevRel):
                    mark = (i, j, r)
                    if mark not in self.markTried:
                        self.markTried.add(mark)
                        return mark
            return (0, 0, 0)

        while True:
            refinementCounter += 1
            currentLevel = refinementCounter
            refineList = self.net.listOfNontractableConstraints()
            if len(refineList) == 0:
                break

            i, j, r = Select(refineList)
            print i, j, r
            if r == 0:
                break
            # save repair point
            self.net.saveBreakpoint(i, j, currentLevel)
            self.triedStack.append((currentLevel, i, j, r))

            # set new value
            self.net.updateConstraint(i, j, r)
            tried = self.aClosureV3([[i, j]])
            if tried == INCONSISTENT:
                self.net.restoreBreakpoint(backjumpLevel)
                s = len(self.triedStack)
                while s > 0:
                    s -= 1
                    level, i, j, r = self.triedStack.pop()
                    if level > backjumpLevel:
                        self.markTried.discard((i, j, r))
                    else:
                        self.triedStack.append((level, i, j, r))
                        break
        print "hsidfs"
        return self.aClosureV3()


alg = Algebra.Allen()

# Load test case
tf = ReadFile.TestFile("test cases/ia_test_instances_10.txt")
# tf = ReadFile.TestFile("test cases/30x500_m_3_allen.csp.txt")
skip = 0
overall = timeit.default_timer()
for graph in tf.processNext():
    if skip > 0:
        skip -= 1
        continue
    net = Network.QCSP(alg, *graph[0])  # First row is always header
    graph = graph[1:]  # remove header
    # create list for very first A-Closure call
    initialConstraints = []
    for A, B, rel in graph:
        net.addConstraint(A, B, rel)
        if rel != net.algebra.Universal:
            initialConstraints.append([A, B])

    print("processing: '%s'" % net.description)
    refinementCounter = 0
    pre = timeit.default_timer()
    valid = Search(net).refinementV2(initialConstraints)
    print("%d Iterations" % refinementCounter)
    print("  > '%s' is %s (%f s)" % (
        net.description, valid, timeit.default_timer() - pre))
    if (net.description.split()[-2] == "NOT" and valid == CONSISTENT) or \
       (net.description.split()[-2] != "NOT" and valid == INCONSISTENT):
        print("!! wrong !!")
        exit(0)
    print("\n\n")
    # break

print("Overall time: %f s\n\n" % (timeit.default_timer() - overall))
