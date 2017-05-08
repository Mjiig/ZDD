import time
import multiprocessing
import statistics
from solvers import zddSolver, dynamic
from validation import bruteforce, instancegenerators

def singleTest(solver, case, queue):
    start = time.time()
    steps = solver(case)[1]
    taken = time.time() - start
    queue.put((steps, taken))

def testSolver(solver, cases):
    queue = multiprocessing.Queue()
    times = []
    stepCounts = []

    for case in cases:
        p = multiprocessing.Process(target=singleTest, args=[solver, case, queue])
        p.start()
        p.join()
        time, steps = queue.get()
        times.append(time)
        stepCounts.append(steps)
    
    return(statistics.mean(times), statistics.variance(times), statistics.mean(stepCounts), statistics.variance(stepCounts))


def tester(size):
    cases = [instancegenerators.randomUnitSquare(size) for _ in range(30)]
    print(size)
    print("zdd {}".format(testSolver(zddSolver.zddTSPSolver, cases)))
    print("dyn {}".format(testSolver(dynamic.dynamicTspSolver, cases)))
        

for size in range(1, 16):
        tester(size)