from random import shuffle
from queue import PriorityQueue
import networkx as nx
from collections import defaultdict

class Bee:
    def __init__(self, coloring, f):
        self.coloring = coloring
        self.f = f

    def __lt__(self, other):
        return self.f.__lt__(other.f)

    def __repr__(self):
        return f"\nFunction: {self.f} Coloring: {self.coloring}"

def generateGraph(ver, d):
    g = nx.watts_strogatz_graph(ver, d, 1)
    graph = {}
    for edge in g.edges:
        u, v = edge
        u += 1
        v += 1
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
    return graph

def findBestPlots(plots, n):
    best = []
    for i in range(n):
        best.append(plots.get())
    return best

def colorGraph(graph, colors):
    coloring = {vertex: 0 for vertex in graph.keys()}
    graph = list(graph.items())
    shuffle(graph)
    colorN = 0
    for vertex, neighbours in graph:
        for color in colors:
            if not neighbourhood(color, neighbours, coloring):
                coloring[vertex] = color
                if color > colorN:
                    colorN += 1
                break
    return coloring, colorN

def generatePlots(graph, plots, n, colors):
    while plots.qsize() < n:
        plot = Bee(*colorGraph(graph, colors))
        if plot not in plots.queue:
            plots.put(plot)

def neighbourhood(color, neighbours, coloring):
    if neighbours:
        for neighbour in neighbours:
            if neighbour in coloring and coloring[neighbour] == color:
                return True
    return False

def discover(plot, graph, foragersN):
    queue = []
    for node, neighbours in sorted(list(graph.items()), key=lambda x: len(x[1]), reverse=True):
        if len(queue) >= foragersN:
            break
        for neighbour in neighbours:
            queue.append((node, neighbour))

    results = []

    for node, neighbour in queue:
        recoloring = dict(plot.coloring)
        recoloring[neighbour], recoloring[node] = recoloring[node], recoloring[neighbour]

        if neighbourhood(recoloring[node], graph[node], recoloring) or \
                neighbourhood(recoloring[neighbour], graph[neighbour], recoloring):
            continue
        else:
            for color in range(1, plot.f + 1):
                if not neighbourhood(color, graph[neighbour], recoloring):
                    recoloring[neighbour] = color
                    results.append(Bee(recoloring, len(set(recoloring.values()))))

    return min(results, key=lambda x: x.f) if results else plot

def foragerSearch(graph, newPlots, plots, n):
    for plot in plots:
        plot = discover(plot, graph, n)
        newPlots.put(plot)

def addBestPlots(plots, bestPlots):
    for plot in bestPlots:
        plots.put(plot)

def main():
    beesN = 60
    scoutsN = 5
    foragerN = beesN - scoutsN
    bestPlotScoutsN = 2
    randomScoutsN = scoutsN - bestPlotScoutsN
    vertices = 300
    degree = 30
    bestForagerN = 20
    randomForagerN = 5
    
    print('Enter your number of bees:')
    beesN = int(input())
    print('Enter your number of scouts:')
    scoutsN = int(input())
    print('Enter your number of best scouts:')
    bestPlotScoutsN = int(input())
    print('Enter your number of vertices in graph:')
    vertices = int(input())
    print('Enter your maximum degree:')
    degree = int(input())
    print('Enter your number of best foragers:')
    bestForagerN = int(input())
    print('Enter your number of random foragers(less than bests):')
    randomForagerN = int(input())

    colors= []
    used_colors = []
    for c in range(50):
        colors.append(c)
        used_colors.append(c)


    graph = generateGraph(vertices, degree)
    plots = PriorityQueue()
    generatePlots(graph, plots, scoutsN, colors)

    for i in range(1001):
        if not i % 20:
            best = plots.get()
            print(f"Iteration {i}, min f: {best.f}")
            plots.put(best)


        bestPlots = findBestPlots(plots, bestPlotScoutsN)
        randomPlots = plots.queue


        plots = PriorityQueue()
        foragerSearch(graph, plots, bestPlots, bestForagerN)
        foragerSearch(graph, plots, randomPlots, randomForagerN)


        bestPlots = findBestPlots(plots, bestPlotScoutsN)
        plots = PriorityQueue()
        generatePlots(graph, plots, randomScoutsN, colors)
        addBestPlots(plots, bestPlots)

    best = plots.get()
    coloring = {k: v for k, v in sorted(best.coloring.items(), key=lambda item: item[0])}
    print(f"Best coloring function: {best.f}\nColoring: {coloring}")

            
            
if __name__ == "__main__":
    main()


