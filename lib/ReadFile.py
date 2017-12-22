#!/usr/bin/env python
import re
import LookupTable


class AlgebraFile(object):
    def __init__(self, path):
        super(AlgebraFile, self).__init__()
        f = open(path)
        self.TName = None
        self.TConverse = None
        self.TComposition = None
        self.baseRelations = None
        self.state = 0
        self.index = 0
        self.lines = f.readlines()
        f.close()
        self.processFile()

    def processFile(self):
        self.baseRelations = self.readBaseRelations()
        self.TName = LookupTable.Nam(self.baseRelations)
        # Process converses
        self.TConverse = LookupTable.Conve(len(self.baseRelations))
        for cv in self.readConverse():
            a = self.TName.getBitmask(cv[0])
            b = self.TName.getBitmask(cv[1])
            self.TConverse.setConverse(a, b)
        # Process compositions
        self.TComposition = LookupTable.Compo(len(self.baseRelations))
        for cp in self.readComposition():  # format: B1 B2 [B1 B2 B3]
            a = self.baseRelations.index(cp[0])
            b = self.baseRelations.index(cp[1])
            c = self.TName.getBitmask(cp[2])
            self.TComposition.setComposition(a, b, c)

    def checkIntegrity(self):
        self.TConverse.checkIntegrity()
        self.TComposition.checkIntegrity()

    def readBaseRelations(self):
        for i in range(self.index, len(self.lines)):
            self.index += 1
            ln = self.lines[i].strip()
            if ln == "interval-relations":
                self.state = 1
            elif self.state == 1:
                return ln.split()
        return "ERROR: no section 'interval-relations' found."

    def readConverse(self):
        for i in range(self.index, len(self.lines)):
            self.index += 1
            ln = self.lines[i].strip()
            if ln == "table of converses":
                self.state = 2
            elif self.state == 2:
                if ln == "" or ln == "composition table":
                    return
                yield ln.split()

    def readComposition(self):
        for i in range(self.index, len(self.lines)):
            self.index += 1
            ln = self.lines[i].strip()
            if ln == "composition table":
                self.state = 3
            elif self.state == 3:
                if ln == "":
                    return
                arr = [x for x in re.split(' |\(|\)', ln) if x is not ""]
                yield [arr[0], arr[1], arr[2:]]


class TestFile(object):
    def __init__(self, path):
        super(TestFile, self).__init__()
        f = open(path)
        self.index = 0
        self.lines = f.readlines()
        f.close()

    def parseHeader(self, line):
        [anz, desc] = line.split("#")
        anz = int(anz)
        desc = desc.strip()
        if anz > 0:
            self.state = 1
            return [anz, desc]
        return [0, "error"]

    def parseConstraint(self, line):
        tmp = line.split()
        rel = tmp[2:]
        if len(rel) == 1:
            rel[0] = rel[0][1:-1]  # remove ()
        else:
            rel[0] = rel[0][1:]     # remove (
            rel[-1] = rel[-1][:-1]  # remove )
        return [int(tmp[0]), int(tmp[1]), rel]

    def processNext(self, verbose=False):
        self.state = 0
        obj = []
        for i in range(self.index, len(self.lines)):
            self.index += 1
            ln = self.lines[i].strip()
            if len(ln) < 3:
                if ln == ".":
                    yield obj
                    obj = []
                    self.state = 0
                continue
            elif self.state == 0:
                [nodes, description] = self.parseHeader(ln)
                obj.append([nodes, description])
                if verbose:
                    print(nodes, description)
            elif self.state == 1:
                [A, B, rel] = self.parseConstraint(ln)
                obj.append([A, B, rel])
                if verbose:
                    print(A, B, rel)
