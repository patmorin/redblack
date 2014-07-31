from __future__ import division
"""Analysing the bottom two levels of a randomly constructed 2-4 tree

This code uses Wormald's Differential Equation Method to study the
distribution of height 2 subtrees that appear in the last two levels
of randomly constructed 2-4 trees.

http://users.monash.edu.au/~nwormald/papers/de.pdf

Specifically, this code studies the following process: We start with a 2-4
tree that contains only the value 0. We then insert a random permutation of 
{1,...,n} into this 2-4 tree using the usual rebalancing rules for 2-4 trees.
This induces a distribution on height 2 subtrees and, as n->infinity, this
distribution converges to some fixed distribution.  It is this distribution
that we determine.
"""
import sys
import math
import fractions
import scipy.linalg
import sympy

"""The following functions are for dealing with the 'types' of height 2
 trees.  

There are 3^2 + 3^3 + 3^4 = 117 possible types. Each type is represented
as a list containing values from the set {2,3,4}.  The number of children
of the root is the length of this list and the values in the list represent
the number of (leaf) children of each child.
"""

def gen_all_types():
    """Generate a list of all 117 possible types."""
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

    # Map types to their indices.
    type_strings = [ type_to_string(t) for t in types ]
    d = dict (zip(type_strings, range(len(type_strings))))

    # Create the output matrix.
    result = [[0 for i in range(len(types))] 
                    for j in range(len(types))]

    # Iterate through each type and see which types it generates when a new
    # leaf is added to it.
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
            for n in new_nodes:
                a = d[type_to_string(n)]
                b = d[type_to_string(t)]
                result[a][b] += p

    # Fill in the diagonal (the only negative entries)
    for i in range(len(types)):
        result[i][i] -= leaves(types[i])  # prob this type is destroyed
        result[i][i] -= 1 # because this is a difference equation

    # The last row is redundant, but the coefficients must sum to 1.
    last_row = result[-1][:]
    for i in range(len(types)):
        result[-1][i] = leaves(types[i])
    
    return result


def get_pawel(solution, types, c):
    """Find the fraction of leaves that have a parent with c children"""
    return sum([solution[i]*c*len([d for d in types[i] if d==c])
                  for i in range(len(types))])


def cost(type):
    """Determine the average cost of traversing a subtree of this type"""
    c = fractions.Fraction(0)
    for i in range(len(type)):
        p = type[i]
        a = [1,fractions.Fraction(5,3),2][type[i]-2]
        c += p*a
        if len(type) == 2 or (len(type) == 3 and i == 0):
            c += p
        else:
            c += 2*p
    c /= leaves(type)
    return c


def print_stats(soln, types):
    """Print some information about a solution"""
    # Sanity check confirms that we get the correct answer for height 1 trees.
    pawel = [get_pawel(soln, types, 2+i) for i in range(3)]
    print "pawel = {}".format(["{}".format(x) for x in pawel])

    alpha = sum(soln)
    print "number of subtrees of height 2 is {}n".format(alpha)
    print "average number of leaves per subtree is {}".format(1/alpha)

    c = sum([soln[i]*leaves(types[i])*cost(types[i]) 
                 for i in range(len(types)) ])
    print "cost of last two levels is {}".format(c)
    print "expected cost is at least log(n) + {}".format(c + math.log(sum(soln),2))


if __name__ == "__main__":
    """Program entry point"""
    types = gen_all_types();
    matrix = conditional_expectations(types)
    rhs = [0]*(len(types)-1) + [1]

    # First solve numerically
    print "Finding floating-point solution...",
    sys.stdout.flush()
    num_soln = scipy.linalg.solve(matrix, rhs)
    print "done."
    print_stats(num_soln, types)

    # Now solve exactly    
    print "Finding exact solution...",
    sys.stdout.flush()
    rat_soln = sympy.Matrix(matrix).LUsolve(sympy.Matrix(rhs))
    print "done."
    print_stats(rat_soln, types)

