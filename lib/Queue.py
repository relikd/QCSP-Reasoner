#!/usr/bin/env python
# coding: utf8
import heapq


class QQueue(object):
    def __init__(self, constraintList):
        super(QQueue, self).__init__()
        self.stack = []
        heapq.heapify(self.stack)
        self.cs = constraintList
        self.previousItem = None

    def dequeue(self):
        var = heapq.heappop(self.stack)
        while var == self.previousItem and len(self.stack) > 0:
            var = heapq.heappop(self.stack)
        # print "get", var
        return var[1]

    def getPriority(self, element):
        constraints = self.cs[element[0]][element[1]]
        # TODO: implement dictionary lookup for priority
        return bin(constraints).count("1")

    def enqueue(self, element):
        prio = self.getPriority(element)
        var = (prio, element)
        # print " -> put", var
        heapq.heappush(self.stack, var)

    def enqueueNew(self, element):
        for x in range(len(self.stack)):
            if self.stack[x][1] == element:
                del self.stack[x]  # cause new priority most likely differ
                break
        self.enqueue(element)

    def isEmpty(self):
        return len(self.stack) == 0
