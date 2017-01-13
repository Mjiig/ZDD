import random
from math import cos, sin, pi

def randomUnitSquare(n):
    ret = []
    for _ in range(n):
        ret.append((random.random(), random.random()))

    return ret

def uniformUnitCircle(n):
    ret = []

    for i in range(n):
        ret.append((cos(2*pi*i/n), sin(2*pi*i/n)))

    return ret
