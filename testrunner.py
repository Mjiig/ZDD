import time
import multiprocessing
import statistics
from solvers import zddSolver, dynamic
from validation import bruteforce, instancegenerators

def singleTest(solver, case, queue):
    start = time.time()
    steps = solver(case)
    taken = time.time() - start
    queue.put((steps[1], steps[2]))

def testSolver(solver, cases):
    queue = multiprocessing.Queue()
    times = []
    stepCounts = []

    for case in cases:
        p = multiprocessing.Process(target=singleTest, args=[solver, case, queue])
        p.start()
        p.join()
        steps, time = queue.get()
        times.append(time)
        stepCounts.append(steps)

    return (statistics.mean(stepCounts), statistics.mean(times)) #times currently doesn't measure time at all...
    
    return(statistics.mean(times), statistics.variance(times), statistics.mean(stepCounts), statistics.variance(stepCounts))


def tester(size):
    cases = [instancegenerators.randomUnitSquare(size) for _ in range(1)]
    print(size)
    print("zdd {}".format(testSolver(zddSolver.zddTSPSolver, cases)))
    #print("dyn {}".format(testSolver(dynamic.dynamicTspSolver, cases)))
        

for size in range(1, 16):
        tester(size)