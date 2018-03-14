#!/usr/bin/env python
# coding: utf8
import re

countBits = [bin(x).count("1") for x in range(1 << 13)]


def calcSubsetScore(bitmask):
    score = 0
    for x in range(13):
        if bitmask & (1 << x):
            score += allenPriority[x]
    return score


allenPriority = [26, 82, 82, 82, 82, 82, 82, 50, 50, 50, 50, 50, 50]
subsetScore = [calcSubsetScore(x) for x in range(1 << 13)]


def powerset(seq):
    if len(seq) <= 0:
        yield []
    else:
        for item in powerset(seq[1:]):
            yield item
            yield [seq[0]] + item


def doubleNested(maxi, start=0):
    for x in range(start, maxi):
        for y in range(start, maxi):
            yield x, y


def tripleNested(maxi, start=0):
    for x in range(start, maxi):
        for y in range(start, maxi):
            for z in range(start, maxi):
                yield x, y, z


def splitTripple(line):
    """ Parse line of the format: "A B (C D E)"
    to array with format: ['A', 'B', ['C', 'D', 'E']] """
    arr = [x for x in re.split(' |\(|\)', line) if x is not ""]
    return [arr[0], arr[1], arr[2:]]


def bits(n):
    """ Iterate over all set bits """
    while n:
        b = n & (~n + 1)
        yield b
        n ^= b
