# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import unittest

import unittest

# Q1 - You have a list of lists. Convert it to a flat list. Only keep the element that's either a string, or an integer that can be divided by 2.
# For example, [[1,2], [3,4, "a"]] to [2,4,"a"]

list_2D = [[1, 2], [3, 4, "a"]]


def Q1(list_2D):
    pass


# Q2 - You have a sequence of items, and you’d like to determine the most frequently occurring items in the sequence. Return them as a tuple (item, # of occurrence). There will only be one unique pair
# For example, ['look', 'into', 'my', 'eyes', 'look'] -> ("look", 2)

words = ['look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
         'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
         'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
         'my', 'eyes', 'you', 'are', 'under']


def Q2(words):
    pass


# Q3 - Use DataFrame from pandas
data = {"name": ["Eric", "Emma", "Ted", "Ashley"],
        "age": [19, 22, 25, 18],
        "score": [95.0, 88.5, 72.0, 91.3]}
# create a pandas DataFrame out of the dictionary

# get the columns as a list

# change the last column names to "final_score"

# sort the df by age, in ascending order

# Q4 - Design a Class DataFrameDemo

"""
 input data is a dictionary, all its keys should be strings, values should be ndarray of the same length
 names = np.array(["Eric", "Emma", "Ted", "Ashley"])
 ages = np.array([19, 22, 25, 18])
 scores = np.array([95.0, 88.5, 72.0, 91.3])
 data = {"name": names , "age": ages, "score": scores}
"""


class DataFrameDemo:

    def __init__(self, data):
        self._check_input_type(data)
        self._check_input_length(data)
        self._data = data

    # check that input data is dictionary, it's keys are strings, values are ndarray
    def _check_input_type(self, data):
        pass

    # check that all ndarray in the input data have the same length
    def _check_input_length(self, data):
        pass

    # return column names as a list, in any order
    def get_columns(self):
        pass

    # return a DataFrame sorted by the column specified
    def sort_by(self, by_column, ascending=True):
        pass


################################################################################################

result1 = Q1(list_2D)
result2 = Q2(words)


class Test(unittest.TestCase):
    def test1_len(self):
        self.assertEqual(len(result1), 3)

    def test1_component(self):
        self.assertTrue("a" in result1)
        self.assertTrue(2 in result1)
        self.assertFalse(5 in result1)

    def test2_istuple(self):
        self.assertTrue(isinstance(result2, tuple))
        self.assertEqual(result2[0], "eyes")
        self.assertEqual(result2[1], 8)


unittest.main()
