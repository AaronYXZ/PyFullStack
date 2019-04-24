# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

import pandas as pd
from collections import defaultdict, Counter
import unittest

# Q1 - You have a list of lists. Convert it to a flat list. Only keep the element that's either a string, or an integer that can be divided by 2.
# For example, [[1,2], [3,4, "a"]] to [2,4,"a"]

list_2D = [[1, 2], [3, 4, "a"]]


def Q1(list_2D):
    result = [x for lst in list_2D for x in lst if (isinstance(x, str) or x % 2 == 0)]
    return result 


# Q2 - You have a sequence of items, and you’d like to determine the most frequently occurring items in the sequence. Return them as a tuple (item, # of occurrence). There will only be one unique pair
# For example, ['look', 'into', 'my', 'eyes', 'look'] -> ("look", 2)

words = ['look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
         'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
         'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
         'my', 'eyes', 'you', 'are', 'under']

def Q2(words):
    word_counts = Counter(words)
    most_common = word_counts.most_common(1)
    return next(iter(most_common))

def Q2(words):
    word_counts = {}
    count = 1
    word = words[0]
    for w in words:
        if w not in word_counts:
            word_counts[w] = 1
        else:
            word_counts[w] += 1
        if word_counts[w] > count:
            count = word_counts[w]
            word = w
    return word, count


# Q3 - Use DataFrame from pandas
data = {"name": ["Eric", "Emma", "Ted", "Ashley"],
        "age": [19, 22, 25, 18],
        "score": [95.0, 88.5, 72.0, 91.3]}
# create a pandas DataFrame out of the dictionary
df = pd.DataFrame(data)

# get the columns as a list
df.columns.tolist()

# change the last column names to "final_score"
df.columns = ["name", "age", "final_score"]

# sort the df by age, in ascending order
df.sort_values(by = "age")

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
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        for col_name, values in data.items():
            if not isinstance(col_name, str):
                raise TypeError("all column names must be strings")
            if not isinstance(values, list):
                raise TypeError("all column values must be list")

    # check that all ndarray in the input data have the same length
    def _check_input_length(self, data):
        pass

    # return column names as a list, in any order
    def get_columns(self):
        pass

    # return a DataFrame sorted by the column specified

    def sort_by(self, by_column, ascending = True):
        pass




###################################################################

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

if  __name__ == '__main__':

    unittest.main()
