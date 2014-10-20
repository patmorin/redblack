"""A simple program to build a 2-4 tree with cost 1.5h

Ultimately, we want to use this to test our partition conjecture.
"""

def binary_tree(h):
    if h == 1:
        return [None, None]
    return [binary_tree(h-1), binary_tree(h-1)]

def bad_tree(h):
    if h == 1:
        return [None, None, None]
    return [binary_tree(h-1), bad_tree(h-1), bad_tree(h-1)] 

def sizes(t):
    d = dict()
    d[id(None)] = 1
    sizes_r(t, d)
    return d
        
def sizes_r(t, d):
    if t is None: return 1
    d[id(t)] = sum([sizes_r(st, d) for st in t])
    return d[id(t)]
 
def cost(t):
    d = sizes(t)
    return cost_r(t, d)/d[id(t)]

def cost_r(t, size):
    if t is None: return 0
    if len(t) == 2 or len(t) == 4:
        return len(t)*size[id(t)]//2 + sum([cost_r(st, size) for st in t])
    else:  # len(t) == 3:
        return size[id(t[0])] + 2*(size[id(t[1])]+size[id(t[2])]) \
               + sum([cost_r(st, size) for st in t])

