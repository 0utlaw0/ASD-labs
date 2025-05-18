import math
import random

random.seed(4206)

def print_matrix(matrix, title="Matrix", line_length=1):
    print(f"\n=== {title} ===")
    for row in matrix:
        print(" ".join(f"{num:{line_length}}" for num in row))  # Each number is line_length characters wide
    print()

def matrix_multiply(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matrix_add(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = A[i][j] + B[i][j]
    return result

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