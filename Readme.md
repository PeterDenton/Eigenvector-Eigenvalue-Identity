# Eigenvector-Eigenvalue Identity Code

This code generates a random Hermitian matrix of dimension n and then calculates the norm squared of the elements of the normed eigenvectors, |v<sub>i,j</sub>|<sup>2</sup>.
It then verifies that it is equivalent to numpy.
To use this code simply run the file as is to numerically verify the formula, or import it into your own code as:

```
import E2
E2.vijsq(H, i, j)
```
returns the norm square of the j<sup>th</sup> element of the i<sup>th</sup> eigenvector where H is a Hermitian matrix of numpy's matrix class, and i and j are indices 0 &le; i,j &le; n.

The new formula is
![E2 Equation](./equation.png)

## References
For further references see [arXiv:1911.xxxxx](https://arxiv.org/abs/1911.xxxxx).
We first discovered this in the context of neutrino oscillations in matter in [arXiv:1907.02534](https://arxiv.org/abs/1907.02534) and presented several proofs in [arXiv:1908.03795](https://arxiv.org/abs/1908.03795).
We believe that the first instance of anything like this expression appeared in Karl Löwner. Über monotone Matrixfunktionen. Math. Z., 38(1):177–216, 1934.
The first instance of this expression seems to have appeared in R. C. Thompson. Principal submatrices of normal and Hermitian matrices. Illinois J. Math., 10:296–308, 1966.
