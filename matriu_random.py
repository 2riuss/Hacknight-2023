import numpy as np
import random
import itertools
import math as m

rand = random.randint(0,m.factorial(9)-1)
permutacions = list(itertools.permutations([0, 1, 2, 3, 4, 5, 6, 7, 8]))

A = [[0,0,0],[0,0,0],[0,0,0]]
vec = list(permutacions[rand])
A[0] = vec[0:3]
A[1] = vec[3:6]
A[2] = vec[6:9]
print(A)


