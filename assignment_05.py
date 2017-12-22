#!/usr/bin/env python3
# coding: utf8
from lib import ReadFile
from lib import LookupTable

# Point Calculus
L = LookupTable.Composition("<", ">", "=")
L.addConverse("=", "=")
L.addConverse("<", ">", True)  # True means bidirectional converse
L.setEquiCompositions()  # set << = <  AND  >> = >  AND == = =
L.addComposition("<", "=", "<", True)  # True means order doesn't matter
L.addComposition(">", "=", ">", True)
L.addComposition("<", ">", ["<", ">", "="], True)
L.checkIntegrity()

N = LookupTable.Names(L.baseRelations)
N.set("SMALLER", "<")
N.set("GREATER", ">")
N.set("EQUAL", "=")
N.set("GREQ", ">", "=")
# N.print_JEPD_set()


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


# Load test case
tf = ReadFile.TestFile("test cases/test_instances_PC.txt")
for graph in tf.processNext():
    print "processing: %s" % graph[0][1]
    for i in range(1, len(graph)):
        r = Relation(*graph[i])
        print r
    break


