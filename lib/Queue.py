#!/usr/bin/env python
# coding: utf8
import Helper

USEHEAP = True
if USEHEAP:
    from heapq import heapify, heappush, heappop
else:
    from collections import deque


class QQueue(object):
    def __init__(self):
        super(QQueue, self).__init__()
        if USEHEAP:  # better for large networks
            self.pq = []
            heapify(self.pq)
        else:
            self.pq = deque([])
            self.entry_finder = set([])

    if USEHEAP:
        def dequeue(self):
            p, r1, r2 = heappop(self.pq)
            return r1, r2

        def enqueue(self, r1, r2, constraint):
            prio = Helper.subsetScore[constraint]
            heappush(self.pq, [prio, r1, r2])

        def isEmpty(self):
            return len(self.pq) == 0

    else:
        def dequeue(self):
            prio, task = self.pq.popleft()
            self.entry_finder.discard(task)
            return task

        def enqueue(self, r1, r2, constraint):
            task = (r1, r2)
            if task not in self.entry_finder:
                self.entry_finder.add(task)
                prio = Helper.subsetScore[constraint]
                self.pq.append([prio, task])
