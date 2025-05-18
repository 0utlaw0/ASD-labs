from matrix import matrix_multiply, matrix_add

def get_undir_degrees(dir):
    return {i: (sum(dir[i]) + sum(dir[j][i] for j in range(len(dir)))) for i in range(len(dir))}

def print_undir_degrees(undir_degree):
    print("\n\n=== Node degrees of undirected graph ===\n")
    print(f"{'== Node ==':^10} {'== Degree ==':^15}\n")
    for index, value in undir_degree.items():
        print(f"{(index + 1):^10}->{value:^15}")
    print()

def get_in_degrees(dir):
    return {i: sum(dir[j][i] for j in range(len(dir))) for i in range(len(dir))}

def get_out_degrees(dir):
    return {i: sum(dir[i]) for i in range(len(dir))}

def print_dir_degrees(in_degree, out_degree):
    print("\n\n=== Node degrees of directed graph ===\n")
    print(f"{'== Node ==':^10}  {'== In-Degree ==':^15}  {'== Out-Degree ==':^15}\n")
    for i in range(len(in_degree)):
        print(f"{(i + 1):^10}->{in_degree[i]:^15}  {out_degree[i]:^15}")
    print()

def is_regular(undir_degrees):
    for i in range(len(undir_degrees)):
        if (undir_degrees[0] != undir_degrees[i]): return (False, 0)
    return (True, undir_degrees[0])

def get_isolated_and_leaf(matrix):
    isolated = []
    leaf = []
    for i in range(len(matrix)):
        if matrix[i] == 0: isolated.append(i + 1)
        if matrix[i] == 1: leaf.append(i + 1)
    return isolated, leaf

def paths_length_2(matrix):
    A2 = matrix_multiply(matrix, matrix)
    paths = []
    
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if A2[i][j] > 0:
                for k in range(len(matrix)):
                    if matrix[i][k] and matrix[k][j]:
                        paths.append(f"{i+1} -> {k+1} -> {j+1}")

    return paths

def paths_length_3(matrix):
    A3 = matrix_multiply(matrix, matrix_multiply(matrix, matrix))
    paths = []
    
    for i in range(len(matrix)):
        for k in range(len(matrix)):
            if A3[i][k] > 0:
                for l in range(len(matrix)):
                    for j in range(len(matrix)):
                        if matrix[i][j] and matrix[j][l] and matrix[l][k]:
                            paths.append(f"{i+1} -> {j+1} -> {l+1} -> {k+1}")

    return paths

def print_paths(paths, length):
    if not paths:  # Check if paths list is empty
        print(f"\nNo paths of length {length} found.")
        return

    print(f"\nPaths of length {length}:")
    line_length = 6  # Number of paths per line
    max_width = max(len(f"({path})") for path in paths)  # Find the widest path

    for i in range(0, len(paths), line_length):
        formatted_paths = [f"({path})".ljust(max_width) for path in paths[i:i + line_length]]
        print(", ".join(formatted_paths) + ",")
    print()

def reachability_matrix(matrix):
    temp = matrix
    reach = matrix

    for _ in range(len(matrix) - 1):
        temp = matrix_multiply(temp, matrix)
        reach = matrix_add(reach, temp)

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if reach[i][j] > 0:
                reach[i][j] = 1
    return reach

import numpy as np
def strong_connectivity_matrix(A):
    R = np.array(A)
    return np.logical_and(R, R.T).astype(int)

def find_strong_components(S, n):
    visited = [False] * n
    components = []

    for v in range(n):
        if not visited[v]:
            component = []
            for u in range(n):
                if S[v, u] == 1:
                    component.append(u + 1)
                    visited[u] = True
            if component:
                components.append(component)
    return components

def condensation_graph(components, dir_matrix):
    condensation = [[0 for _ in range(len(components))] for _ in range(len(components))]
    for i, comp_i in enumerate(components):
        for j, comp_j in enumerate(components):
            if i != j:
                for v in comp_i:
                    for u in comp_j:
                        if dir_matrix[v - 1][u - 1] == 1:
                            condensation[i][j] = 1
                            break
    return condensation