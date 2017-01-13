import math

from itertools import permutations

def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def cost(path):
    c = 0
    last = path[0]
    for city in path[1:]:
        c += dist(last, city)
        last = city

    return c

def tspSolver(cities):
    best = cost(cities)
    for path in permutations(cities):
        if cost(path) < best:
            best = cost(path)

    return best
