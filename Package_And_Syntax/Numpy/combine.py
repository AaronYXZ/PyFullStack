import numpy as np

"""
np.vstack https://docs.scipy.org/doc/numpy/reference/generated/numpy.vstack.html
"""
arr1 = [1,2,3,4]
arr2 = [5,6,7,8]

v_arr = np.vstack((arr1, arr2)) # also takes array
print(v_arr)
h_arr = np.hstack((arr1, arr2))
print(h_arr)
