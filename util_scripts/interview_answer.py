# Libraries Included:
# Numpy, Scipy, Scikit, Pandas

from collections import defaultdict, Counter
import unittest

# Q1 - You have a list of lists. Convert it to a flat list. Only keep the element that's either a string, or an integer that can be divided by 2.
# For example, [[1,2], [3,4, "a"]] to [2,4,"a"]

list_2D = [[1, 2, 3], ["a", 4, 5], ["b", 6]]


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



# Q4 - Design a Class
#   __init__(self, data):
#      _check_


###################################################################

result1 = Q1(list_2D)
result2 = Q2(words)




class Test_Q1(unittest.TestCase):
    def test1_len(self):
        self.assertEqual(len(result1), 5)

    def test1_component(self):
        self.assertTrue("a" in result1)
        self.assertTrue("b" in result1)
        self.assertTrue(2 in result1)
        self.assertFalse(1 in result1)

    def test2_istuple(self):
        self.assertTrue(isinstance(result2, tuple))
        self.assertEqual(result2[0], "eyes")
        self.assertEqual(result2[1], 8)

if  __name__ == '__main__':

    unittest.main()
