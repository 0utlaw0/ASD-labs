from graph_utility import *
from matrix_utility import *

n1 = 4
n2 = 2
n3 = 0
n4 = 6

n = n3 + 10

k = 1.0 - n3 * 0.01 - n4 * 0.005 - 0.05

dir = get_dir(n, k)

undir = get_undir(dir)
print_matrix(undir, "Undirected Graph")

B = get_B(n)

C = get_C(undir, B)

D = get_D(C)

H = get_H(D)

W = get_W(C, D, H)
print_matrix(W, "W Matrix", 3)

def get_MinimumSpanningTree(W):
    n = len(W)
    in_mst = [False] * n
    MST = list()
    
    in_mst[0] = True
    
    for _ in range(n-1):
        min_weight = math.inf
        min_edge = (-1, -1)

        for u in range(n):
            if in_mst[u]:
                for v in range(n):
                    if not in_mst[v] and W[u][v] != math.inf and W[u][v] < min_weight:
                        min_weight = W[u][v]
                        min_edge = (u, v)
        
        if min_edge[0] != -1:
            MST.append(min_edge)
            in_mst[min_edge[1]] = True

    return MST

MST = get_MinimumSpanningTree(W)

def get_weight(W, MST):
    weight = 0
    for edge in MST:
        weight += W[edge[0]][edge[1]]
    return weight

total_weight = get_weight(W, MST)

print("Minimum Spanning Tree Edges:")
for edge in MST:
    print(f"{edge[0] + 1} - {edge[1] + 1}")
print()

print(f"Total Weight of Minimum Spanning Tree: {total_weight}")

draw_graph(undir, directed=False, title="Minimum Spanning Tree", weight_matrix=W, spanning_tree=MST)