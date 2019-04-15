
import re
import random

# https://stackoverflow.com/questions/19306976/python-shuffling-with-a-parameter-to-get-the-same-result
if __name__ == '__main__':
    seed1 = 1
    seed2 = 10
    lst = list(range(10))
    lst2 = list(range(10))
    random.Random(seed1).shuffle(lst)
    random.Random(seed2).shuffle(lst2)
    for x, y in zip(lst, lst2):
        # assert x == y, "should be equal"
        print("x is {}, y is {}".format(x, y))


