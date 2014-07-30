from __future__ import division
"""Analysing the bottom two levels of a randomly constructed 2-4 tree"""
import math
import numpy
import fractions
import scipy.linalg
from sympy import *

def gen_all_types():
    """Generate all 2-4 trees of height 2.

    There are 3^2 + 3^3 + 3^4 = 117 of these trees"""
    all_types = []
    for c in range(2, 5):
        t = [2]*c
        types = [t[:]]
        while t != [4]*c:
            i = 0
            while t[i] == 4:
                t[i] = 2
                i += 1
            t[i] += 1
            types.append(t[:])
        all_types += types
    return all_types

def type_to_string(t):
    """Convert a type to a string."""
    return "".join([str(i) for i in t])

def string_to_type(s):
    """Convert a string to a type."""
    return tuple([int(c) for c in s])

def children(t):
    """Determine how many children a type has."""
    return len(t)

def leaves(t):
    """Determine how many leaves a type has."""
    return sum(t)

def conditional_expectations(types):    
    """Compute the conditional expectation matrix.

    This sets up a matrix, M, such that the vector x that satisfies 
    Mx=[0,0,0,...,0,1] gives the distribution of node types.  In 
    particular, the number of height 2 subtrees of type types[i] is
    a.a.s n*x[i]
    """

    type_strings = [ type_to_string(t) for t in types ]
    d = dict (zip(type_strings, range(len(type_strings))))
    result = [[0 for i in range(len(types))] 
                    for j in range(len(types))]

    # Iterate through each type and see which types it generates.
    for i in range(len(types)):
        t = types[i]
        for j in range(len(t)):
            p = t[j]
            t2 = t[:]
            t2[j] += 1
            if type_to_string(t2) in d:
                # No splitting happening
                new_nodes = [t2]
            else:
                # We created a 5-node, split it
                t2[j] = 3
                t2.insert(j, 2)
                if len(t2) <= 4:
                    # split doesn't propagate
                    new_nodes = [t2]
                else:
                    # We created another 5-node, split it
                    new_nodes = [t2[:2], t2[2:]]
            #print "{} => {} with probability {}".format(t, new_nodes, p)    
            for n in new_nodes:
                a = d[type_to_string(n)]
                b = d[type_to_string(t)]
                result[a][b] += p

    # Remember that this is a difference equation.
    for i in range(len(types)):
        result[i][i] -= 1 + leaves(types[i])

    # The last row is redundant, but the coefficients must sum to 1 (t).
    last_row = result[-1][:]
    for i in range(len(types)):
        result[-1][i] = leaves(types[i])
    
    return result

def get_height1_prob(solution, types, c):
    """Find the fraction of leaves that have a parent with c children"""
    return sum([solution[i]*c*len([d for d in types[i] if d==c])
                  for i in range(len(types))])

def cost(type):
    """Determine the average cost of traversing a subtree of this type"""
    c = 0
    for i in range(len(type)):
	p = type[i]
        a = [1,5/3,2][type[i]-2]
        c += p*a
        if len(type) == 2 or (len(type) == 3 and i == 0):
	    c += p
        else:
            c += 2*p
    c /= leaves(type)
    return c
    
if __name__ == "__main__":
    types = gen_all_types();
    matrix = conditional_expectations(types)
    
    print "{:<15}".format(""),
    print "".join(["{:>4}".format(type_to_string(types[r])) 
                   for r in range(len(matrix))])
    for r in range(len(matrix)):
        if r < len(types): print "{:<15}".format(types[r]),
        else: print "{:<15}".format(""),
        print "".join([ "{:>4}".format(entry) for entry in matrix[r] ])
    solution = scipy.linalg.solve(matrix, [0]*(len(matrix)-1) + [1])
    
    # Sanity check confirms that we get the correct answer for height 1 trees.
    pawel = [get_height1_prob(solution, types, 2+i) for i in range(3)]
    rat_pawel = [fractions.Fraction(x).limit_denominator(10000) for x in pawel]
    print "pawel = {}".format(["{}".format(x) for x in rat_pawel])

    print "number of subtrees of height 2 is {}n".format(sum(solution))

    print "average number of leaves per subtree is {}".format(
      sum([solution[i]*leaves(types[i]) for i in range(len(types))])
          / sum(solution))

    c = sum([solution[i]*leaves(types[i])*cost(types[i]) for i in range(len(types)) ])
    print "cost of last two levels is {}".format(c)


    print "expected cost is at least log(n) + {}".format(c + math.log(sum(solution),2))



''' This is some old code, from when I thought the ordering of children
    didn't matter.
def _kill_gen_all_types():
    """Generate all possible types of height 2 nodes"""
    return gen_types(2) + gen_types(3) + gen_types(4)

def _kill_gen_types(i):
    """Generate all the binom(i+1,2) possible types of an i-node"""
    return [ [y+2 for y in x] for x in _gen_types(i, 2) ]

def _kill_gen_types(i, ticks):
    """Implement gen_types recursively."""
    if (i < 0): return []
    if (ticks == 0): return [ [0]*i ]
    return [ [y+1 for y in x] for x in _gen_types(i, ticks-1)] \
         + [ [0] + x for x in _gen_types(i-1, ticks) ]
'''


