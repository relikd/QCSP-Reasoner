#!/usr/bin/env python3
# coding: utf8
from lib import Algebra, ReadFile, Helper
import timeit


class Network(object):
    def __init__(self, algebra, maxIndex, description):
        super(Network, self).__init__()
        self.algebra = algebra
        self.nodeCount = maxIndex + 1
        self.csCount = 0
        self.description = description
        self.cs = [[self.algebra.Universal
                   for a in range(self.nodeCount)]
                   for b in range(self.nodeCount)]

    def enforceOneConsistency(self, symbol):
        bitmask = self.algebra.bitmaskFromList([symbol])
        for i in range(self.nodeCount):
            self.cs[i][i] = bitmask

    def addConstraint(self, nodeA, nodeB, constraint):
        if nodeA >= self.nodeCount or nodeB >= self.nodeCount:
            print "Error: Adding Relation to Network (Max Index)"
        else:
            constraintMask = self.algebra.bitmaskFromList(constraint)
            self.cs[nodeA][nodeB] = constraintMask
            # if self.cs[nodeB][nodeA] == self.algebra.Universal:
            #     self.cs[nodeB][nodeA] = self.algebra.converse(constraintMask)

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
                    # print i, j, k, Cik_star
                    self.cs[i][k] = Cik_star
                    if Cik_star == 0:
                        return False  # early exit
                    s = True
        return True

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


algFile = ReadFile.AlgebraFile("algebra/point_calculus.txt")
# algFile = ReadFile.AlgebraFile("algebra/allen.txt")
alg = Algebra.Algebra(algFile)
# print alg.TName
alg.checkIntegrity()
print "\n"

# Load test case
tf = ReadFile.TestFile("test cases/test_instances_PC.txt")
# tf = ReadFile.TestFile("test cases/ia_test_instances_10.txt")
for graph in tf.processNext():
    net = Network(alg, *graph[0])  # First row is always header
    # if net.description != "instance 0: NOT consistent":
    #     continue
    for i in range(1, len(graph)):
        net.addConstraint(*graph[i])

    print "processing:", net
    net.enforceOneConsistency("=")
    # net.enforceOneConsistency("EQ")

    pre = timeit.default_timer()
    consistent = net.aClosureV1()
    print timeit.default_timer() - pre
    # print "Done:", net
    print "  > Is", net.description, "consistent? ", consistent
