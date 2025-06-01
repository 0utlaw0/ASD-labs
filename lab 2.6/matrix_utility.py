import math
import random

random.seed(4217)

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

def get_undir(dir):
    result = [[0] * len(dir) for _ in range(len(dir))]
    for i in range(len(dir)):
        for j in range(len(dir)):
            result[i][j] = result[j][i] = max(dir[i][j], dir[j][i])
    return result

def get_B(n):
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = random.uniform(0, 2.0)
    return result

def get_C(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = math.ceil(B[i][j] * 100 * A[i][j])
    return result

def get_D(C):
    n = len(C)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if C[i][j] != 0:
                result[i][j] = 1
    return result

def get_H(D):
    n = len(D)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if D[i][j] != D[j][i]:
                result[i][j] = 1
    return result

def get_W(C, D, H):
    n = len(C)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i < j:
                W = C[i][j] * (D[i][j] + H[i][j])
                result[i][j] = W if W != 0 else math.inf
                result[j][i] = result[i][j]
    return result