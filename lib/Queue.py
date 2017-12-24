#!/usr/bin/env python
# coding: utf8
import heapq


class QQueue(object):
    def __init__(self):
        super(QQueue, self).__init__()
        self.stack = []
        heapq.heapify(self.stack)
        self.previousItem = None

    def init(self):
        self.previousItem = heapq.heappop(self.stack)

    def dequeue(self):
        var = heapq.heappop(self.stack)
        while var == self.previousItem and len(self.stack) > 0:
            var = heapq.heappop(self.stack)
        # return var[1]
        retVal = self.previousItem[1]
        self.previousItem = var
        return retVal

    def enqueueNew(self, element):
        var = (element[1] % 4, element)
        # for x in self.stack:
        #     if x[1] == var[1]:
        #         return
        # if var in self.stack:
        #     return
        heapq.heappush(self.stack, var)

    def isEmpty(self):
        return len(self.stack) == 0
