from __future__ import division
import random
from math import log

class Node(object):
    def __init__(self, children):
        self.size = sum([size(x) for x in children])
        self.children = children

    def __str__(self):
        return ",".join([str(size(x)) for x in self.children])

def split(n):
    a = n.children
    n.children = a[:2]
    n.size = sum([size(x) for x in n.children])
    return Node(a[2:])

def add(n):
    if n is None: 
        return None
    # Pick a random child (weighted by size).
    i = random.randrange(size(n))
    c = -1
    while i >= 0:
        c += 1
        i -= size(n.children[c])

    child = add(n.children[c])
    n.size += 1

    # If return value is a new node, add it to our list of children.
    if child is None or child is not n.children[c]:
        n.children.insert(c+1, child)

    # Split this node if it's too big.
    if len(n.children) == 5:
        return split(n)
    return n

def size(n):
    if n is None: return 1
    return n.size

if __name__ == "__main__":
    root = Node([None, None])
    for i in range(200000):
        r = add(root)
        if r is not root:
            root = Node([root, r])
            n = size(root)
            print "{:>7.5} {:>7.5}".format(size(root.children[0])/n,
                                      size(root.children[1])/n),
            print "{:>9} {:>5.3}".format(n, log(n,2))


