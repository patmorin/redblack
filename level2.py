from __future__ import division
"""Analysing the bottom two levels of a randomly constructed 2-4 tree"""
import numpy
import scipy.linalg
from sympy import *

def gen_all_types():
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

''' Pffft - from before I thought order didn't matter
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

def type_to_string(t):
    """Convert a type to a string."""
    return "".join([str(i) for i in t])

def string_to_type(s):
    """Convert a string to a type."""
    return tuple([int(c) for c in s])

def children(t):
    """Determine how many children a type has"""
    return len(t)

def leaves(t):
    """Determine how many leaves a type has."""
    return sum(t)

def conditional_expectations(types):    
    """Compute the conditional expectation of type t."""

    type_strings = [ type_to_string(t) for t in types ]
    d = dict (zip(type_strings, range(len(type_strings))))
    result = [[0 for i in range(len(types))] 
                    for j in range(len(types))]

    # Iterate through each node type and account for the types that it can
    # generate.
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
                # We create a 5-node, split it
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
    for j in range(len(types)):
        result[j][j] -= 1

    # The last row is redundant, but the coefficients must sum to 1.
    last_row = result[-1][:]
    for i in range(len(types)):
        result[-1][i] = leaves(types[i])
    
    return result

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
    print scipy.linalg.solve(matrix, [0]*(len(matrix)-1) + [1])

