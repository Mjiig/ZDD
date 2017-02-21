import itertools
import math
# Use itertools.combinations instead
def combinations(items, n):
    if n==0:
        yield set()
        return
    if n > len(items):
        return
    
    x = {items[0]}
    items = items[1:]

    for comb in combinations(items, n-1):
        yield x | comb
    yield from combinations(items, n)

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def tryCombinations(items, n):
    if n == 1:
        return {frozenset([x]): {x:0} for x in items}
    ret = {}
    costs = tryCombinations(items, n-1)
    for comb in itertools.combinations(items, n):
        comb = frozenset(comb)
        ret[comb] = {}
        for city in comb:
            ret[comb][city] = min(costs[comb-{city}][s]+dist(city, s) for s in comb-{city})
    return ret

def dynamicTspSolver(items):
    costs = tryCombinations(items, len(items))[frozenset(items)]
    return min(costs.values())
