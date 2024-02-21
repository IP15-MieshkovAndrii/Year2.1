import random as rand

def improvementRand(c, graph):
    nodes = []
    i = 0
    for gene in c.chromosome:
        i+=1
        if gene:
            nodes.append(i)

    rand.shuffle(nodes)
    for node in nodes:
        adjacentNodes = graph[node]
        rand.shuffle(adjacentNodes)
        for adjacentNode in adjacentNodes:
            if adjacentNode in nodes:
                continue

            if set(nodes) <= set(graph[adjacentNode]):
                chromosome = list(c.chromosome)
                chromosome[adjacentNode-1] = 1
                c.update(chromosome)
                return


def improvementHeuristic(c, graph):
    nodes = []
    for i, gene in enumerate(c.chromosome):
        if gene:
            nodes.append(i + 1)

    rand.shuffle(nodes)
    adjacentNodes = []
    for node in nodes:
        adjacentNodes += graph[node]

    adjacentNodes = list(set(adjacentNodes))
    rand.shuffle(adjacentNodes)

    for adjacentNode in sorted(adjacentNodes, key=lambda x: len(graph[x])):
        if adjacentNode in nodes:
            continue
        if set(nodes) <= set(graph[adjacentNode]):
            chromosome = list(c.chromosome)
            chromosome[adjacentNode-1] = 1
            c.update(chromosome)
            return