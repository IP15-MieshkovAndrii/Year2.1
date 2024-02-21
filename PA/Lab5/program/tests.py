from main import clique
import crossingover, mutation, local

def testCrossingOver():
    funcs = {crossingover.onePoint: (0,0,0,0), crossingover.twoPoint: (0,0,0,0),crossingover.uniform: (0,0,0,0)}
    for func in funcs:
        print(f"Function: Crossing over - {func.__name__}")
        a,b,c,stuck = 0,0,0,0
        for i in range(10):
            print(f"\nTest number {i+1}")
            result = clique(func, mutation.onePoint, local.improvementRand)
            a += result[0]
            b += result[1]
            c += result[2]
            if result[2] == 100000:
                stuck += 1

        funcs[func] = (a / 10, b / 10, c / 10, stuck)

    for func, results in funcs.items():
        print(func.__name__, ":", results[3], ":", results[0], results[1], results[2])

def testMutation():
    funcs = {mutation.onePoint: (0,0,0,0),mutation.interval: (0,0,0,0)}
    for func in funcs:
        print(f"Function: Mutation - {func.__name__}")
        a,b,c,stuck = 0,0,0,0
        for i in range(10):
            print(f"\nTest number {i+1}")
            result = clique(crossingover.onePoint, func, local.improvementRand)
            a += result[0]
            b += result[1]
            c += result[2]
            if result[2] == 100000:
                stuck += 1

        funcs[func] = (a / 10, b / 10, c / 10, stuck)

    for func, results in funcs.items():
        print(func.__name__, ":", results[3], ":", results[0], results[1], results[2])

def testLocal():
    funcs = {local.improvementRand: (0,0,0,0),local.improvementHeuristic: (0,0,0,0)}
    for func in funcs:
        print(f"Function: Local - {func.__name__}")
        a,b,c,stuck = 0,0,0,0
        for i in range(10):
            print(f"\nTest number {i+1}")
            result = clique(crossingover.onePoint, mutation.onePoint, func)
            a += result[0]
            b += result[1]
            c += result[2]
            if result[2] == 100000:
                stuck += 1

        funcs[func] = (a / 10, b / 10, c / 10, stuck)

    for func, results in funcs.items():
        print(func.__name__, ":", results[3], ":", results[0], results[1], results[2])
if __name__ == "__main__":
    # testCrossingOver()
    # testMutation()
    testLocal()