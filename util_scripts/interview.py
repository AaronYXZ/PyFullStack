# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import unittest

# Q1 - You have a list of lists. Convert it to a flat list. For example, [[1,2], [3,4]] to [1,2,3,4]

list_2D = [[1, 2, 3], ["a", 4, 5], ["b", 6]]


def Q1(list_2D):
    pass


# Q2 - You have a sequence of items, and you’d like to determine the most frequently occurring items in the sequence.

words = ['look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
         'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
         'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
         'my', 'eyes', "you're", 'under']

def Q2():
    pass


# Q4 - Design a Class
#   __init__(self, data):
#      _check_


list_1D = Q1(list_2D)


class Test(unittest.TestCase):
    def test_len(self):
        self.assertEqual(len(list_1D), 5)

    def test_component(self):
        self.assertTrue("a" in list_1D)
        self.assertTrue("b" in list_1D)
        self.assertTrue(2 in list_1D)
        self.assertFalse(1 in list_1D)

# unittest.main()
