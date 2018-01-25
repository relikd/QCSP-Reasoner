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
        self.stack = [["lol", 0]]
        self.lastModified = [[[0]
                             for a in range(self.net.nodeCount)]
                             for b in range(self.net.nodeCount)]

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

    def aClosureV3(self, arcs=None):
        global backjumpLevel
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
                Ckj = self.net.cs[k][j]
                Cki = self.net.cs[k][i]
                Cik_star = Cik & self.net.algebra.compose(Cij, Cjk)
                Ckj_star = Ckj & self.net.algebra.compose(Cki, Cij)
                if Cik_star == 0 or Ckj_star == 0:
                    backjumpLevel = max(
                        self.lastModified[k][i][0], self.lastModified[k][j][0],
                        self.lastModified[i][k][0], self.lastModified[j][k][0],
                        self.lastModified[i][j][0], self.lastModified[j][i][0])
                    return INCONSISTENT  # early exit
                if Cik_star != Cik:
                    self.stack.append([i, k, Cik])
                    # self.stack.append([k, i, Cki])
                    self.net.cs[i][k] = Cik_star
                    q.enqueueNew(i, k, Cik_star)
                    # self.net.cs[k][i] &= self.net.algebra.converse(Cik_star)
                    # q.enqueueNew(k, i)
                if Ckj_star != Ckj:
                    self.stack.append([k, j, Ckj])
                    # self.stack.append([j, k, Cjk])
                    self.net.cs[k][j] = Ckj_star
                    q.enqueueNew(k, j, Ckj_star)
                    # self.net.cs[j][k] &= self.net.algebra.converse(Ckj_star)
                    # q.enqueueNew(j, k)
        return CONSISTENT

    def refinementV2(self, E=None):
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

        for c, i, j in refineList:
            prevRel = self.net.cs[i][j]
            # for baseRel in Helper.bits(prevRel):
            for baseRel in self.net.algebra.aTractableSet(prevRel):
                self.stack.append(["lol", currentLevel])
                self.stack.append([i, j, self.net.cs[i][j]])
                if self.lastModified[i][j][0] < currentLevel:
                    self.lastModified[i][j].insert(0, currentLevel)

                self.net.cs[i][j] = baseRel
                if self.refinementV2([[i, j]]) == CONSISTENT:
                    return CONSISTENT

                if currentLevel > backjumpLevel and backjumpLevel > 0:
                    return INCONSISTENT

                while len(self.stack) > 0:  # restore previous state
                    itm = self.stack.pop()
                    if itm[0] == "lol":
                        if backjumpLevel == 0 or itm[1] == backjumpLevel:
                            break
                        continue
                    self.net.cs[itm[0]][itm[1]] = itm[2]
                    if backjumpLevel > 0:
                        modifyArr = self.lastModified[itm[0]][itm[1]]
                        while modifyArr[0] > backjumpLevel:
                            del(modifyArr[0])
        return INCONSISTENT


alg = Algebra.Allen()

# Load test case
# tf = ReadFile.TestFile("test cases/test_instances_PC.txt")
tf = ReadFile.TestFile("test cases/ia_test_instances_10.txt")
# tf = ReadFile.TestFile("test cases/test_generated1.txt")
skip = 0
overall = timeit.default_timer()
for graph in tf.processNext():
    net = Network.QCSP(alg, *graph[0])  # First row is always header
    if skip > 0:
        skip -= 1
        continue
    for i in range(1, len(graph)):
        net.addConstraint(*graph[i])
    net.initNontractableRelations()

    print("processing: '%s'" % net.description)
    refinementCounter = 0
    pre = timeit.default_timer()
    # valid = Search(net).aClosureV2()
    valid = Search(net).refinementV2()
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
