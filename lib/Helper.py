#!/usr/bin/env python
# coding: utf8


def powerset(seq):
    if len(seq) <= 0:
        yield []
    else:
        for item in powerset(seq[1:]):
            yield item
            yield [seq[0]] + item


def doubleNested(maxi):
    for x in range(maxi):
        for y in range(maxi):
            yield (x, y)


def tripleNested(maxi):
    for x in range(maxi):
        for y in range(maxi):
            for z in range(maxi):
                yield (x, y, z)
