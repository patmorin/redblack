"""A simulation of randomly-built 2-4 trees."""
from __future__ import division
import random
from math import log

"""This class represents a simulated node in a 2-4 tree.

Each instance of this class maintains a list of its children and
its subtree size.
"""
class Node(object):
    def __init__(self, children):
        self.size = sum([size(x) for x in children])
        self.children = children

    def __str__(self):
        return ",".join([str(size(x)) for x in self.children])

def split(n):
    """Split the 5-node n into a 2-node and 3-node.

    n becomes a 2-node and we return a new 3-node.
    """
    a = n.children
    n.children = a[:2]
    n.size = sum([size(x) for x in n.children])
    return Node(a[2:])

def add(n):
    """Add a new node to the subtree rooted at n.

    The position of the node is chosen uniformly at random from each 
    of the size(n) possible positions. (We exclude the leftmost position)
    """
    if n is None: 
        return None
    # Pick a random child (weighted by size).
    i = random.randrange(size(n))
    c = -1
    while i >= 0:
        c += 1
        i -= size(n.children[c])

    # Recursively add to this child.
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
    """Return the size of the subtree rooted at n"""
    if n is None:
        return 1
    return n.size

if __name__ == "__main__":
    root = Node([None, None])
    print "{:^15} {:^15}".format("predicted", "actual")
    print "{:>7} {:>7}".format("a", "b"),
    print "{:>7} {:>7}".format("a", "b")
    print " "*15,
    for i in range(260000):
        r = add(root)
        if r is not root:
            root = Node([root, r])
            n = size(root)
            a = size(root.children[0])/n
            b = size(root.children[1])/n
            print "{:>7.5} {:>7.5}".format(a, b),
            print "{:>9} {:>5.3}".format(n, log(n,2))
            if a > b:
                ap = (2/5+6/25)*a
                bp = a-ap + bp
            elif a < (2/5)*b:
                ap = a + (4/25)*b
                bp = (21/25)*b
            else:
                (ap, bp) = (a, b)
            print "{:>7.5} {:>7.5}".format(ap, bp),


