#!/usr/bin/env python3
# coding: utf8
from lib import Algebra, ReadFile, Helper, Queue
import timeit


class Network(object):
    def __init__(self, algebra, maxIndex, description):
        super(Network, self).__init__()
        self.algebra = algebra
        self.nodeCount = maxIndex + 1
        self.description = description
        self.cs = [[self.algebra.Universal
                   for a in range(self.nodeCount)]
                   for b in range(self.nodeCount)]

    def enforceOneConsistency(self, symbol):
        bitmask = self.algebra.bitmaskFromList([symbol])
        for i in range(self.nodeCount):
            self.cs[i][i] = bitmask

    def addConstraint(self, A, B, constraint):
        if A >= self.nodeCount or B >= self.nodeCount:
            print "ERROR: Adding Relation to Network (Max Index)"
            return
        constraintMask = self.algebra.bitmaskFromList(constraint)
        converseRelation = self.algebra.converse(constraintMask)
        self.cs[A][B] = constraintMask
        if self.cs[B][A] == self.algebra.Universal:
            self.cs[B][A] = converseRelation
        elif not (self.cs[B][A] & converseRelation):
            print "ERROR: Adding inconsistent constraint:", \
                A, B, constraint, "::", self.description
            self.cs[A][B] = 0

    def aClosureV1(self):
        s = True
        while s:
            s = False
            for (i, j, k) in Helper.tripleNested(self.nodeCount):
                # print "processing", i, j, k
                Cij = self.cs[i][j]
                Cjk = self.cs[j][k]
                Cik = self.cs[i][k]
                # if Cij != self.algebra.Universal and\
                #    Cjk != self.algebra.Universal:
                Cik_star = Cik & self.algebra.compose(Cij, Cjk)
                if Cik != Cik_star:
                    self.cs[i][k] = Cik_star
                    s = True
                if Cik_star == 0:
                    return "Inconsistent"  # early exit
        return "Consistent"

    def aClosureV2(self, arcs=[]):
        q = Queue.QQueue()
        if len(arcs) == 0:
            for (i, j) in Helper.doubleNested(self.nodeCount):
                q.enqueueNew([i, j])
        else:
            for arc in arcs:
                q.enqueueNew(arc)
        q.init()
        while not q.isEmpty():
            (i, j) = q.dequeue()
            for k in range(self.nodeCount):
                if k == i or k == j:
                    continue
                Cij = self.cs[i][j]
                Cjk = self.cs[j][k]
                Cik = self.cs[i][k]
                Cik_star = Cik & self.algebra.compose(Cij, Cjk)
                if Cik_star != Cik:
                    self.cs[i][k] = Cik_star
                    q.enqueueNew([i, k])
                Ckj = self.cs[k][j]
                Cki = self.cs[k][i]
                Ckj_star = Ckj & self.algebra.compose(Cki, Cij)
                if Ckj_star != Ckj:
                    self.cs[k][j] = Ckj_star
                    q.enqueueNew([k, j])
                if Cik_star == 0 or Ckj_star == 0:
                    return "Inconsistent"  # early exit
        return "Consistent"

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


# algFile = ReadFile.AlgebraFile("algebra/point_calculus.txt")
algFile = ReadFile.AlgebraFile("algebra/allen.txt")
alg = Algebra.Algebra(algFile)
# print alg
alg.checkIntegrity()
print "\n"

# Load test case
# tf = ReadFile.TestFile("test cases/test_instances_PC.txt")
tf = ReadFile.TestFile("test cases/ia_test_instances_10_simple.txt")
for graph in tf.processNext():
    net = Network(alg, *graph[0])  # First row is always header
    # if net.description != "test-inconsistent-3":
    #     continue
    for i in range(1, len(graph)):
        net.addConstraint(*graph[i])

    # print "processing:", net
    # net.enforceOneConsistency("=")
    net.enforceOneConsistency("EQ")

    pre = timeit.default_timer()
    valid = net.aClosureV2()
    print timeit.default_timer() - pre
    # print "Resulting QCSP:", net
    print "  >", net.description, "is:", valid
    # print alg
    break
