import numpy as np
from functools import reduce


# Calculate the norm square of the jth element of the ith eigenvector using the alternate algorithm
# H is a square np.matrix
def vij_sq(H, i, j):
    # Get the size of the matrix
    n = H.shape[0]

    # Get the eigenvalues of the matrix using numpy
    eigenvalues = np.linalg.eigvalsh(H)

    # Determine the jth minor
    Mj = np.delete(np.delete(H, j, 0), j, 1)

    # Get the eigenvalues of the minor
    minor_eigenvalues = np.linalg.eigvalsh(Mj)

    # Calculate the numerator
    numerator = 1.
    for k in range(n - 1):
        numerator *= eigenvalues[i] - minor_eigenvalues[k]

    # Calculate the denominator
    denominator = 1.
    for k in range(n):
        if k == i:
            continue
        denominator *= eigenvalues[i] - eigenvalues[k]

    return numerator / denominator


def eig_sq(H):
    # Get the size of the matrix
    n = H.shape[0]
    res = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            res[i, j] = vij_sq(H, j, i)

    return res


# Calculate the norm square with performance improvements
def vij_sq_perf(H, i, j):
    # Get the size of the matrix
    n = H.shape[0]

    # Get the eigenvalues of the matrix using numpy
    eigenvalues = np.linalg.eigvalsh(H)

    # Determine the jth minor
    Mj = np.delete(np.delete(H, j, 0), j, 1)

    # Get the eigenvalues of the minor
    minor_eigenvalues = np.linalg.eigvalsh(Mj)

    # Calculate the numerator
    eigenvaluei = eigenvalues[i]
    numerator = reduce(lambda x, y: x * y, [eigenvaluei - minor_eigenvalues[k] for k in range(n - 1)])

    # Calculate the denominator
    denominator = reduce(lambda x, y: x * y, [eigenvaluei - eigenvalues[k] for k in range(n) if k != i])

    return numerator / denominator


def eig_sq_perf(H):
    # Get the size of the matrix
    n = H.shape[0]
    res = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            res[i, j] = vij_sq_perf(H, j, i)

    return res


# Calculate the norm square of all the elements of all the eigenvectors using numpy's built in eigenvector calculator
# H is a square np.matrix
def eig_sq_np(H):
    # Get the eigenvalues and eigenvalues of the matrix
    eigenvalues, eigenvectors = np.linalg.eigh(H)
    return abs(eigenvectors) ** 2


# Prints true for each element that agrees between the E2 method and the method built into numpy
# H is a square np.matrix
# mode determines comparison with normal or improved function
def compare(H, mode=0):
    # The tolerance for comparison purposes
    tol = 1e-12

    # Select function depending upon the value of mode
    if mode == 0:
        res = eig_sq(H)
    elif mode == 1:
        res = eig_sq_perf(H)

    # Return the comparison matrix
    return abs(res - eig_sq_np(H)) < tol


if __name__ == "__main__":
    # Generate a random Hermitian matrix
    # Dimension of the matrix
    n = 8
    H = np.random.rand(n, n) + 1j * np.random.rand(n, n)
    H = 0.5 * (H + H.T)

    # Print the second element of the first eigenvector as calculated in both methods
    print("\n--- using the algorithm ---")
    basic = eig_sq(H)
    print("basic implementation: ", basic[0, 1])
    perf = eig_sq_perf(H)
    print("performant implementation: ", perf[0, 1])

    print("\n--- using numpy ---")
    nump = eig_sq_np(H)
    print(nump[0, 1])