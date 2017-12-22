#!/usr/bin/env python
# coding: utf8
import re


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


def splitTripple(line):
    """ Parse line of the format: "A B (C D E)"
    to array with format: ['A', 'B', ['C', 'D', 'E']] """
    arr = [x for x in re.split(' |\(|\)', line) if x is not ""]
    return [arr[0], arr[1], arr[2:]]
