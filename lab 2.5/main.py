from graph_utility import draw_graph
import random
import math

n1 = 4
n2 = 2
n3 = 0
n4 = 6

n = n3 + 10

k = 1.0 - n3*0.01 - n4*0.005 - 0.15

random.seed(4206)

def print_matrix(matrix, title="Matrix", line_length=1):
    print(f"\n=== {title} ===")
    for row in matrix:
        print(" ".join(f"{num:{line_length}}" for num in row))  # Each number is line_length characters wide
    print()

def get_dir(n, k):
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = math.floor(random.uniform(0, 2.0) * k)
    return result

def bfs_tree(graph, start):
    visited = [False] * len(graph)
    levels = [-1] * len(graph)  
    queue = []
    queue.append(start)
    visited[start] = True
    levels[start] = 0  
    bfs_tree = [[0] * len(graph) for _ in range(len(graph))]
    steps = []  
    
    current_level = 0
    nodes_at_current_level = 1  
    nodes_at_next_level = 0     
    
    while queue:
        steps.append({
            "visited": [i + 1 for i, v in enumerate(visited) if v], 
            "queue": [q + 1 for q in queue],
            "levels": [levels[i] for i in range(len(levels))],
            "current_level": current_level
        })
        
        node = queue.pop(0)
        nodes_at_current_level -= 1
        
        for neighbor in range(len(graph)):
            if graph[node][neighbor] and not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
                levels[neighbor] = current_level + 1
                nodes_at_next_level += 1
                bfs_tree[node][neighbor] = 1
        
        
        if nodes_at_current_level == 0:
            current_level += 1
            nodes_at_current_level = nodes_at_next_level
            nodes_at_next_level = 0

    return bfs_tree, steps

def dfs_tree(graph, start):
    visited = [False] * len(graph)
    stack = [(start, -1)]  
    dfs_tree = [[0] * len(graph) for _ in range(len(graph))]
    steps = []  

    while stack:
        node, parent = stack.pop()
        if not visited[node]:
            visited[node] = True
            
            steps.append({"visited": [i + 1 for i, v in enumerate(visited) if v], "queue": [node + 1]})
            
            
            if parent != -1:
                dfs_tree[parent][node] = 1
                
            for neighbor in range(len(graph) - 1, -1, -1):  
                if graph[node][neighbor] and not visited[neighbor]:  
                    stack.append((neighbor, node))

    return dfs_tree, steps

dir = get_dir(n, k)

bfs, bfs_steps = bfs_tree(dir, 0)
dfs, dfs_steps = dfs_tree(dir, 0)

print_matrix(dir, "Directed Graph")
print_matrix(bfs, "BFS Tree")
print_matrix(dfs, "DFS Tree")

draw_graph(dir, directed=True, title="Original Directed Graph")

print("\nBFS Vertex order:")
print("Vertex number -> Order number")
draw_graph(bfs, directed=True, title="BFS Tree", graph_type="bfs", steps=bfs_steps)
print()

print("\nDFS Vertex order:")
print("Vertex number -> Order number")
draw_graph(dfs, directed=True, title="DFS Tree", graph_type="dfs", steps=dfs_steps)
print()