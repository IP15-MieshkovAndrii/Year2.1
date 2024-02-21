import random as rand


def onePoint(c):
    i = rand.randint(0, len(c.chromosome)-1)
    chromosome = list(c.chromosome)
    chromosome[i] = 0 if chromosome[i] else 1
    c.update(chromosome)


def interval(c):
    chromosome = list(c.chromosome)
    point1 = rand.randint(0, len(chromosome)-2)
    point2 = rand.randint(point1, len(chromosome))
    for i in range(point1, point2):
        chromosome[i] = 0 if chromosome[i] else 1
    c.update(chromosome)