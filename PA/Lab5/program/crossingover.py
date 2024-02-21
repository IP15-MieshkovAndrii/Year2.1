import random as rand
from individual import Individual

def onePoint(a, b):
    graph = a.graph
    a, b = a.chromosome, b.chromosome
    point = rand.randint(0, len(a)-1)
    newChromosome = a[:point+1] + b[point+1:]
    return Individual(newChromosome, graph)


def twoPoint(a, b):
    graph = a.graph
    a, b = a.chromosome, b.chromosome
    point1 = rand.randint(0, len(a)//2)
    point2 = rand.randint(point1, len(b) - 1)
    newChromosome = a[:point1 + 1] + b[point1 + 1:point2+1] + a[point2+1:]
    return Individual(newChromosome, graph)

def uniform(a, b):
    chromosome = []
    graph = a.graph
    a, b = a.chromosome, b.chromosome
    for x, y in zip(a, b):
        chromosome += rand.choice([x, y]),
    return Individual(chromosome, graph)


