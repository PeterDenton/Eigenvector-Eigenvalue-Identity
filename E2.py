import numpy as np
from functools import reduce

# Calculate the norm square of the jth element of the ith eigenvector using the alternate algorithm
# H is a square np.matrix
# i,j are integers between 0 and n-1, inclusive
def vijsq(H, i, j):
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
		if k == i: continue
		denominator *= eigenvalues[i] - eigenvalues[k]
	return numerator / denominator
#Calculate the norm square with performance improvements
def vijsqperf(H, i, j):
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
	numerator = reduce( lambda x, y: x*y, [eigenvaluei - minor_eigenvalues[k] for k in range(n-1)])
	# Calculate the denominator
	denominator = reduce( lambda x, y: x*y, [eigenvaluei - eigenvalues[k] for k in range(n) if k!= i])
	return numerator / denominator


# Calculate the norm square of the jth element of the ith eigenvector using numpy's built in eigenvector calculator
# H is a square np.matrix
# i,j are integers between 0 and n-1, inclusive
def vijsq_np(H, i, j):
	# Get the eigenvalues and eigenvalues of the matrix
	eigenvalues, eigenvectors = np.linalg.eigh(H)
	return abs(eigenvectors[j, i]) ** 2

# Prints true for each element that agrees between the E2 method and the method built into numpy
# H is a square np.matrix
# mode determines comparison with normal or improved function
def compare(H, mode = 0):
	# Get the size of the matrix
	n = H.shape[0]
	# The tolerance for comparison purposes
	tol = 1e-12
	# The matrix that will be returned
	res = np.empty((n, n), dtype = np.bool)
	for i in range(n):
		for j in range(n):
			# Fill in the matrix with True or False depending on if they agree or not
			if mode != 0:
				res[i, j] = abs(vijsqperf(H, i, j) - vijsq_np(H, i, j)) < tol
			else:
				res[i, j] = abs(vijsq(H, i, j) - vijsq_np(H, i, j)) < tol
	return res

if __name__ == "__main__":
	# Generate a random Hermitian matrix
	# Dimension of the matrix
	n = 8
	H = np.random.rand(n, n) + 1j * np.random.rand(n, n)
	H = np.matrix(H)
	H = 0.5 * (H + H.H)

	# Print the second element of the first eigenvector as calculated in both methods
	print(vijsq(H, 0, 1))
	print(vijsq_np(H, 0, 1))
	# Print the comparison of the two methods, should be a matrix full of Trues
	print(compare(H))
