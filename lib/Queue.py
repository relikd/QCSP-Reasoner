#!/usr/bin/env python
# coding: utf8
import heapq
import Helper


class QQueue(object):
    def __init__(self, constraintList):
        super(QQueue, self).__init__()
        self.stack = []
        heapq.heapify(self.stack)
        self.cs = constraintList

    def dequeue(self):
        p, r1, r2 = heapq.heappop(self.stack)
        return r1, r2

    def getPriority(self, r1, r2):
        # TODO: implement dictionary lookup for priority
        return Helper.countBits(self.cs[r1][r2])
        # return bin(self.cs[r1][r2]).count("1")

    def enqueue(self, r1, r2):
        prio = self.getPriority(r1, r2)
        heapq.heappush(self.stack, [prio, r1, r2])

    def enqueueNew(self, r1, r2):
        for x in range(len(self.stack)):
            if self.stack[x][1] == r1 and self.stack[x][2] == r2:
                del self.stack[x]  # cause new priority most likely differ
                break
        self.enqueue(r1, r2)

    def isEmpty(self):
        return len(self.stack) == 0
