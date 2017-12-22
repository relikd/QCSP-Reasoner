#!/usr/bin/env python
import Helper


class AlgebraFile(object):
    def __init__(self, path):
        super(AlgebraFile, self).__init__()
        f = open(path)
        self.state = 0
        self.index = 0
        self.lines = f.readlines()
        f.close()

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
                yield Helper.splitTripple(ln)


class TestFile(object):
    def __init__(self, path):
        super(TestFile, self).__init__()
        f = open(path)
        self.index = 0
        self.lines = f.readlines()
        f.close()

    def parseHeader(self, line):
        [anz, desc] = line.split("#")
        if int(anz) > 0:
            self.state = 1
            return [int(anz), desc.strip()]
        return [0, "error"]

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
                [A, B, rel] = Helper.splitTripple(ln)
                obj.append([int(A), int(B), rel])
                if verbose:
                    print(A, B, rel)
