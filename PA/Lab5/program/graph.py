import random as rand
from itertools import combinations


def generateGraph(n, p, maxDegree, minDegree):
    nodes = list(range(1, n+1))
    graph = {node: [] for node in nodes}
    pEdges = combinations(nodes, 2)
    for u, v in pEdges:
        if rand.random() < p and len(graph[v]) < maxDegree and len(graph[u]) < maxDegree:
            graph[u].append(v)
            graph[v].append(u)
    for node, edges in graph.items():
        if len(edges) < minDegree:
            nodes.remove(node)
            edges.append(rand.choice(nodes))
    return graph

# def dump_graph(ver, p, maxD, minD):
#     graph = generateGpaph(ver, p, maxD, minD)
#     with open("__graph_", "w") as f:
#         f.write(str(graph))
#     nodes_n = len(graph)
#     return graph, nodes_n

# def load_graph():
#     with open("graph", "r") as f:
#         graph = eval(f.read())
#     nodes_n = len(graph)
#     return graph, nodes_n