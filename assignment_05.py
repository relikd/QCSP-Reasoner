#!/usr/bin/env python3
# coding: utf8
from lib import ReadFile, Helper


class Network(object):
    def __init__(self, maxIndex, description):
        super(Network, self).__init__()
        self.nodeCount = maxIndex + 1
        self.csCount = 0
        self.description = description
        self.cs = [["U"
                   for a in range(self.nodeCount)]
                   for b in range(self.nodeCount)]

    def addConstraint(self, rel):
        if rel.A >= self.nodeCount or rel.B >= self.nodeCount:
            print "Error: Adding Relation to Network (Max Index)"
        else:
            self.cs[rel.A][rel.B] = rel.symbols
            if self.cs[rel.B][rel.A] == "U":
                self.cs[rel.B][rel.A] = rel.symbols

    def compose(self, relA, relB):
        for a in relA:
            for b in relB:
                print a, b

    def aClosure(self):
        s = True
        while s:
            s = False
            for (i, j, k) in Helper.tripleNested(self.nodeCount):
                print "processing", i, j, k
                self.cs[i][j]

    def __str__(self):
        relCount = 0
        s = ""
        for (a, b) in Helper.doubleNested(self.nodeCount):
            if self.cs[a][b] != "U":
                s += "%d {%s} %d\n" % (a, ','.join(self.cs[a][b]), b)
                relCount += 1
        return "%s (%d nodes, %d relations)\n%s" % (
            self.description, self.nodeCount, relCount, s)


class Relation(object):
    def __init__(self, A, B, rel):
        super(Relation, self).__init__()
        self.A = A
        self.B = B
        self.symbols = frozenset(rel)

    def complement(self):
        c = self.symbols.symmetric_difference(self.algebra.baseRelations)
        return Relation(self.A, self.B, c)

    def __str__(self):
        return "%s {%s} %s" % (self.A, ','.join(self.symbols), self.B)


alg = ReadFile.AlgebraFile("algebra/point_calculus.txt")
print alg.TName
alg.checkIntegrity()
print "\n"

# Load test case
tf = ReadFile.TestFile("test cases/test_instances_PC.txt")
for graph in tf.processNext():
    net = Network(*graph[0])  # First row is always header
    for i in range(1, len(graph)):
        net.addConstraint(Relation(*graph[i]))
    print "processing:", net
    net.aClosure()
    break
