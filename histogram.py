from __future__ import division

import sys

if __name__ == "__main__":
    lines = open(sys.argv[1]).read().splitlines()
    data = [line.split() for line in lines]
    data = [float(x[0]) for x in data]
    n = len(data)
    mini = min(data)
    maxi = max(data)
    rangei = maxi-mini
    nb = 100
    bs = rangei / nb
    histogram = [0]*nb
    for x in data:
        histogram[min(nb-1,int((x-mini)//bs))] += 1
    for i in range(len(histogram)):
        print "{} {}".format(mini+i*bs, histogram[i]/n)

