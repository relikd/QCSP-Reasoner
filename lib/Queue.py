#!/usr/bin/env python
# coding: utf8
from collections import deque


class QQueue(object):
    def __init__(self):
        super(QQueue, self).__init__()
        self.pq = deque([])
        self.entry_finder = set([])

    def dequeue(self):
        task = self.pq.popleft()
        self.entry_finder.discard(task)
        return task

    def enqueue(self, r1, r2):
        task = (r1, r2)
        if task not in self.entry_finder:
            self.entry_finder.add(task)
            self.pq.append(task)
