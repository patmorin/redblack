from __future__ import division
from fractions import Fraction

def do_splits(a):
    print ":".join(str(x) for x in a)
    while len(a) < 5:
        j = 0
        for i in range(len(a)):
            if a[i] > a[j]: j = i
        a.insert(j, 2*a[j]/5)
        a[j+1] = 3*a[j+1]/5
        print ":".join(str(x) for x in a)
    b = [sum(a[:2]), sum(a[2:])]
    print ":".join(str(x) for x in b)

