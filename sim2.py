"""A simulation of randomly-built 2-4 trees.

This variant keeps track of the average cost of the tree at all times."""
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
        self.fix_cost()

    def fix_cost(self):
        if len(self.children) != 3:
            self.cost = self.size*(len(self.children)//2) \
                            + sum([cost(c) for c in self.children])
        else:
            self.cost = 2*self.size - size(self.children[0]) \
                        + sum([cost(c) for c in self.children])

    def __str__(self):
        return ",".join([str(size(x)) for x in self.children])


def cost(n):
    if n is None:
        return 0
    return n.cost


def split(n):
    """Split the 5-node n into a 2-node and 3-node.

    n becomes a 2-node and we return a new 3-node.
    """
    a = n.children
    n.children = a[:2]
    n.size = sum([size(x) for x in n.children])
    n.fix_cost()
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
    n.fix_cost()

    # If return value is a new node, add it to our list of children.
    if child is None or child is not n.children[c]:
        n.children.insert(c+1, child)
    n.fix_cost()

    # Split this node if it's too big.
    if len(n.children) == 5:
        return split(n)
    return n


def size(n):
    """Return the size of the subtree rooted at n"""
    if n is None:
        return 1
    return n.size


def size_check(n):
    """Do a recursive check of all size values stored in n's subtree"""
    if n is None:
        s = 1
    else:
        s = sum([size_check(u) for u in n.children])
    assert(s == size(n))
    return s 

      
def cost_check(n):
    """Do a recursive check of all cost values stored in n's subtree"""
    if n is None: 
        c = 0
    elif len(n.children) == 2:
        c = n.size + sum([cost_check(u) for u in n.children])
    elif len(n.children) == 3:
        c = 2*sum([size(u) for u in n.children]) \
                 - size(n.children[0]) \
                 + sum([cost_check(u) for u in n.children])
    else:
        c = 2*n.size + sum([cost_check(u) for u in n.children])
    assert(c == cost(n))
    return c


def lsb(i):
    """Return the index of the least significant bit of i"""
    if i == 0: return None
    j = 0
    while i & (1 << j) == 0:
        j += 1
    return j

def power_of_two(i):
    """Return True if and only if i is a power of 2"""
    if i == 0: return False
    return 1 << lsb(i) == i


def node_histogram(n, h, hist):
    if n == None:
        return
    hist[h][len(n.children)-2] += 1
    for u in n.children:
        node_histogram(u, h+1, hist)

def enum_level(n, d, level):
    if d == level:
        yield n
    elif d < level:
        for u in n.children:
            for w in enum_level(u, d+1, level): 
                yield w

if __name__ == "__main__":

    # Start with a single binary root node.
    height = 1
    root = Node([None, None])

    # Add n elements
    for i in range(2000000):
        n = size(root)
        c = cost(root)
        #print "{:10} {:10} {:10} {:10} {:10}\r" \
        #        .format(c, n, c/n, (c/n)/log(n,2), (c/n)-log(n,2))
        r = add(root)

        # Check if root was split.
        if r is not root:
            height += 1
            root = Node([root, r])

        # Do spot checking to make sure calculations are correct.
        if power_of_two(i):
            size_check(root)
            cost_check(root)
    print

    print "n = {}, height = {}".format(size(root), height)

    print "Distribution of nodes at various levels"
    histogram = [[0, 0, 0] for h in range(height)]
    node_histogram(root, 0, histogram)
    for h in range(height):
        nh = sum(histogram[h])
        print "h:{:>3} {} ({} nodes)".format(h, [x/nh for x in histogram[h]], nh)

    # print the subtree sizes at one particular level
    print "Subtree sizes:"
    level = [n for n in enum_level(root, 0, height-7)]
    threes = [n for n in enum_level(root, 0, height-8) if len(n.children)==3]
    lo3 = [n.children[0] for n in threes]
    print "Average size of node is {}".format(
            sum([size(n) for n in level])/len(level) )
    print "Average size of first-child-of-3-node is {}".format(
            sum([size(n) for n in lo3])/len(lo3) )
    oo3 = [n.children[1] for n in threes] + [n.children[2] for n in threes]
    print "Average size of other-child-of-3-node is {}".format(
            sum([size(n) for n in oo3])/len(oo3) )




