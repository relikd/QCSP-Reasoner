#!/usr/bin/env python
# coding: utf8
import heapq
import Helper


class QQueue(object):
    def __init__(self):
        super(QQueue, self).__init__()
        self.stack = []
        heapq.heapify(self.stack)

    def dequeue(self):
        p, r1, r2 = heapq.heappop(self.stack)
        return r1, r2

    def enqueue(self, r1, r2, constraint):
        prio = Helper.subsetScore[constraint]  # Helper.countBits[constraint]
        heapq.heappush(self.stack, [prio, r1, r2])

    def enqueueNew(self, r1, r2, constraint):
        # for x in range(len(self.stack)):
        #     if self.stack[x][1] == r1 and self.stack[x][2] == r2:
        #         del self.stack[x]  # cause new priority most likely differ
        #         break
        self.enqueue(r1, r2, constraint)

    def isEmpty(self):
        return len(self.stack) == 0
