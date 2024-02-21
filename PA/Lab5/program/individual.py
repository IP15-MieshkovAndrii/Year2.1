class Individual:
    def __init__(self, chromosome, graph):
        self.chromosome = chromosome
        self.graph = graph
        self.f = self.maxClique(chromosome)

    def maxClique(self, chromosome):
        nodes = []
        i = 0
        for gene in chromosome:
            i+=1    
            if gene:
                nodes.append(i)
        for node in nodes:
            for adjacentNode in nodes:
                if node == adjacentNode:
                    continue
                else:
                    if adjacentNode not in self.graph[node]:
                        return 0
        return len(nodes)

    def update(self, chromosome):
        self.chromosome = chromosome
        self.f = self.maxClique(chromosome)

    def __lt__(self, other):
        return self.f.__lt__(other.f)

    def __gt__(self, other):
        return self.f.__gt__(other.f)

    def __le__(self, other):
        return self.f.__le__(other.f)

    def __ge__(self, other):
        return self.f.__ge__(other.f)

    def __repr__(self):
        return f"{self.f}"

    def __eq__(self, other):
        return self.chromosome == other.chromosome