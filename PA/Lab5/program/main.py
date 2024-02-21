from graph import *
import random as rand
from individual import Individual
import crossingover, mutation, local

def createPopulation(population, graph):
    nodeN = len(graph)
    for i in range(nodeN):
        chromosome = [0 for x in range(nodeN)]
        chromosome[i] = 1
        population.append(Individual(chromosome, graph))
    return 1

def Parents(population):
    a = max(population)
    b = rand.choice(population)
    while a == b:
        b = rand.choice((population))
    return a, b

def removeWorstSol(population):
    minimum = []
    m = population[0].f
    for individ in population:
        if individ.f < m:
            minimum.clear()
            m = individ.f
            minimum.append(individ)
        elif individ.f == m:
            minimum.append(individ)
    population.remove(rand.choice(minimum))

def clique(crossingOverF, mutationF, localeF):
    a = b = c = 100000
    MUTATION = 0.25
    ver = 300
    maxD = 30
    minD = 2
    print('Enter your vertices number:')
    ver = int(input())
    print('Enter your max degree:')
    maxD = int(input())
    print('Enter your min degree:')
    minD = int(input())
    graph = generateGraph(ver, 0.9, maxD, minD)
    population = []
    record = createPopulation(population, graph)

    for i in range(100000):
        if not i%10000:
            print(f"Iteration: {i}")

        parents = Parents(population)
        kid = crossingOverF(*parents)

        if rand.random() <= MUTATION:
            mutationF(kid)

        if not kid.f:
            continue

        localeF(kid, graph)

        if kid.f > record:
            record = kid.f
            print(f"Iteration: {i}, f:{record}")
            if record == 15:
                a = i
            if record == 16:
                b = i
            if record >= 17:
                c = i
                break

        if kid not in population:
            population += kid,
            removeWorstSol(population)
    print(f"Best solution: {record}")
    return a, b, c



if __name__ == '__main__':
    print('Enter your crossing over(onePoint - 1, twoPoint - 2, uniform - 3):')
    co = int(input())
    print('Enter your mutation(onePoint - 1, interval - 2):')
    m = int(input())
    print('Enter your local(improvementRand - 1, improvementHeuristic - 2):')
    l = int(input())
    cof = [crossingover.onePoint, crossingover.twoPoint, crossingover.uniform]
    mf = [mutation.onePoint, mutation.interval]
    lf = [local.improvementRand, local.improvementHeuristic]
    clique(cof[co-1], mf[m-1], lf[l-1])