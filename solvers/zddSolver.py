from zdd import nodeset
from zdd import node
from zdd.operations import Operations

def zddTSPSolver(cities):
    n = len(cities)
    # (i, j) means that at the ith step, the jth city was visited
    variables = [(a,b) for a in range(n) for b in range(n)]
    ns = nodeset.NodeSet(variables)
    assertions = {x: ns.assertVariable(x) for x in variables}
    negations = {x: Operations.negation(assertions[x]) for x in variables}

    current = ns.tautology()

    for i in range(n):
        line = ns.contradiction()
        for j in range(n):
            line = Operations.disjunction(line, assertions[(i,j)])
        current = Operations.conjunction(current, line)
        print(i)

    for i in range(n):
        at_time = ns.tautology()
        for j in range(n):
            given_city = ns.tautology()
            for k in range(j+1, n):
                given_city = Operations.conjunction(given_city, negations[(i,k)])
            imp = Operations.implication(assertions[(i,j)], given_city)
            at_time = Operations.conjunction(at_time, imp)
        current = Operations.conjunction(current, at_time)
        print(i)

    for j in range(n):
        for_city = ns.tautology()
        for i in range(n):
            given_time = ns.tautology()
            for k in range(i+1, n):
                given_time = Operations.conjunction(given_time, negations[(k,j)])

            imp = Operations.implication(assertions[(i,j)], given_time)
            for_city = Operations.conjunction(for_city, imp)
        current = Operations.conjunction(current, for_city)
        print(j)

    return current