# https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html
import numpy as np
"""
Generates a random sample from a given 1-D array

New in version 1.7.0.

Parameters:	
a : 1-D array-like or int
If an ndarray, a random sample is generated from its elements. If an int, the random sample is generated as if a were np.arange(a)

size : int or tuple of ints, optional
Output shape. If the given shape is, e.g., (m, n, k), then m * n * k samples are drawn. Default is None, in which case a single value is returned.

replace : boolean, optional
Whether the sample is with or without replacement

p : 1-D array-like, optional
The probabilities associated with each entry in a. If not given the sample assumes a uniform distribution over all entries in a.

Returns:	
samples : single item or ndarray
The generated random samples
"""

# generate a uniform random sample from np.aragne(5) of size 3
arr1 = np.random.choice(5,3)
assert isinstance(arr1, np.ndarray)
# >>> #This is equivalent to np.random.randint(0,5,3)

# generate a non-uniform random sample
np.random.seed(123)
arr2 = np.random.choice(5, 3, p=[0.1, 0, 0.3, 0.6, 0])

# this is equivalent to list of [0,1,2,3,4]
np.random.seed(123)
arr3 = np.random.choice([0,1,2,3,4], 3, p=[0.1, 0, 0.3, 0.6, 0])

np.testing.assert_array_equal(arr2, arr3)


# generate a uniform random sample from np.arange(5) of size 3 without replacement:

np.random.choice(5, 3, replace=False)

# Any of the above can be repeated with an arbitrary array-like instead of just integers. For instance:
aa_milne_arr = ['pooh', 'rabbit', 'piglet', 'Christopher']
arr_str = np.random.choice(aa_milne_arr, 5, p=[0.5, 0.1, 0.1, 0.3])
assert isinstance(arr_str, np.ndarray)
assert arr_str.dtype == "<U11"