#!/usr/bin/env python3
# coding: utf8
from lib import Algebra, ReadFile, Helper, Network, Queue
import timeit
import copy

CONSISTENT = "CONSISTENT"
INCONSISTENT = "INCONSISTENT"
refinementCounter = 0


class Search(object):
    def __init__(self, network):
        super(Search, self).__init__()
        self.net = network

    def aClosureV1(self):
        s = True
        while s:
            s = False
            for (i, j, k) in Helper.tripleNested(self.net.nodeCount):
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
        q = Queue.QQueue(self.net.cs)
        if arcs is None:
            for (i, j) in Helper.doubleNested(self.net.nodeCount):
                q.enqueue([i, j])
        else:
            for arc in arcs:
                q.enqueue(arc)

        while not q.isEmpty():
            (i, j) = q.dequeue()
            for k in range(self.net.nodeCount):
                if k == i or k == j:
                    continue
                Cij = self.net.cs[i][j]
                Cjk = self.net.cs[j][k]
                Cik = self.net.cs[i][k]
                Cik_star = Cik & self.net.algebra.compose(Cij, Cjk)
                if Cik_star != Cik:
                    self.net.cs[i][k] = Cik_star
                    q.enqueueNew([i, k])
                    self.net.cs[k][i] &= self.net.algebra.converse(Cik_star)
                    q.enqueueNew([k, i])
                Ckj = self.net.cs[k][j]
                Cki = self.net.cs[k][i]
                Ckj_star = Ckj & self.net.algebra.compose(Cki, Cij)
                if Ckj_star != Ckj:
                    self.net.cs[k][j] = Ckj_star
                    q.enqueueNew([k, j])
                    self.net.cs[j][k] &= self.net.algebra.converse(Ckj_star)
                    q.enqueueNew([j, k])
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

        refineList = C_star.listOfMultiRelationConstraints()
        if len(refineList) == 0:  # all rel's have 1 base relation
            if Search(C_star).aClosureV2() == CONSISTENT:
                # print("Resulting QCSP:\n%s" % C_star)
                return CONSISTENT
        for rel in refineList:
            conn = C_star.nodeConnectivity[rel[0]]\
                + C_star.nodeConnectivity[rel[1]]
            rel.insert(0, conn)
        refineList.sort(reverse=True)

        # print refineList
        for (c, i, j) in refineList:
            prevRel = C_star.cs[i][j]
            for baseRel in Helper.bits(prevRel):
                C_star.cs[i][j] = baseRel
                if Search(C_star).refinementV15([[i, j]]) == CONSISTENT:
                    return CONSISTENT
            # ASK: if correct
            # C_star.cs[i][j] = prevRel

        return INCONSISTENT


# algFile = ReadFile.AlgebraFile("algebra/point_calculus.txt")
algFile = ReadFile.AlgebraFile("algebra/allen.txt")
alg = Algebra.Algebra(algFile)
# print(alg)
alg.checkIntegrity()
print("\n")

# Load test case
# tf = ReadFile.TestFile("test cases/test_instances_PC.txt")
tf = ReadFile.TestFile("test cases/ia_test_instances_10.txt")
skip = 0
overall = timeit.default_timer()
for graph in tf.processNext():
    net = Network.QCSP(alg, *graph[0])  # First row is always header
    if skip > 0:
        skip -= 1
        continue
    for i in range(1, len(graph)):
        net.addConstraint(*graph[i])

    # preprocessing
    net.calculateNodeConnectivity()
    # net.enforceOneConsistency("=")
    net.enforceOneConsistency("EQ")

    print("processing: '%s'" % net.description)
    refinementCounter = 0
    pre = timeit.default_timer()
    # valid = Search(net).aClosureV2()
    valid = Search(net).refinementV15()
    print("%d Iterations" % refinementCounter)
    print("  > '%s' is %s (%f s)" % (
        net.description, valid, timeit.default_timer() - pre))
    if (net.description.split()[-2] == "NOT" and valid == CONSISTENT) or \
       (net.description.split()[-2] != "NOT" and valid == INCONSISTENT):
        print("!! wrong !!")
        # exit(0)
    print("\n\n")
    # break

print("Overall time: %f s\n\n" % (timeit.default_timer() - overall))
