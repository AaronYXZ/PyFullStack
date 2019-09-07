"""
函数shuffle与permutation都是对原来的数组进行重新洗牌（即随机打乱原来的元素顺序）；
区别在于shuffle直接在原来的数组上进行操作，改变原来数组的顺序，无返回值。而permutation不直接在原来的数组上进行操作，
而是返回一个新的打乱顺序的数组，并不改变原来的数组。
原文：https://blog.csdn.net/lyy14011305/article/details/76207327

"""

import numpy as np

arr_ori = np.array([1,2,3,4,5])
arr_copy = arr_ori.copy()
np.random.shuffle(arr_ori)
print(arr_ori)
arr_per = np.random.permutation(arr_copy)
print(arr_per)
print(arr_copy)