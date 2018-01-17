#!/usr/bin/python
import random
import sys

baseRels = ["EQ", "B", "BI", "D", "DI", "O",
            "OI", "M", "MI", "S", "SI", "F", "FI"]

# A(n, d, l)
# n - size of network (# of var's)
# d - average degree (avg. # of non-universal constraint relations)
# l - average label size


def randomLabel(l):
    R = [x for x in baseRels if random.uniform(0, 1) < (
        l / float(len(baseRels)))]
    if (len(R) == 0):
        R = [baseRels[random.randint(0, len(baseRels) - 1)]]
    return R


def generateNetwork(n, d, l):
    for i in range(0, n + 1):
        for j in range(i, n + 1):
            if ((i != j) and random.uniform(0, 1) < (float(d) / float(n - 1))):
                print("%d %d (%s)" % (i, j, " ".join(randomLabel(l))))
    print(".")


def multipleNetworks(C, N, D, L):
    for i in range(0, C):
        print("%d # instance %d: NOT consistent" % (N, i))
        generateNetwork(N, D, L)


def main():
    if len(sys.argv) == 5:
        C = int(sys.argv[1])
        N = int(sys.argv[2])
        D = int(sys.argv[3])
        L = int(sys.argv[4])
        multipleNetworks(C, N, D, L)
    else:
        print("Usage:  'generateQCSP C N D L'\n"
              " C  Number of networks to be generated\n"
              " N  Number of nodes in the network\n"
              " D  Average degree (# of outgoing relations per node)\n"
              " L  Average label size (# of base relations)\n")
        multipleNetworks(1, 5, 2, 2)


main()
