import collections
from collections.abc import Iterable, Iterator
import unittest

lst = [1,2,3]
st = (1,2,3)
dic = {"a": 1, "b":2}

"""
check generic syntax - iterable vs iterator 
Iterable is an object that has an __iter__ method which returns an Iterator, or which defines a __getitem__ method
Iterator is an object that with __next__ method
"""
class test_iterable_iterator(unittest.TestCase):
    def test_iterable_iterator(self):
        """
        Iterator is subclass of Iterable, not vice versa
        """
        self.assertFalse(issubclass(Iterable, Iterator))
        self.assertTrue(issubclass(Iterator, Iterable))

    def test_iterable_1(self):
        """
        list, set, tuple and dictionary are Iterable
        deque, defaultdict, OrderedDict and Counter from collections are Iterable
        """
        self.assertTrue(issubclass(list, Iterable))
        self.assertTrue(issubclass(set, Iterable))
        self.assertTrue(issubclass(dict, Iterable))
        self.assertTrue(issubclass(tuple, Iterable))
        self.assertTrue(issubclass(collections.defaultdict, Iterable))
        self.assertTrue(issubclass(collections.deque, Iterable))
        self.assertTrue(issubclass(collections.OrderedDict, Iterable))
        self.assertTrue(issubclass(collections.Counter, Iterable))

        self.assertTrue(isinstance(lst, Iterable))
        self.assertTrue(isinstance(st, Iterable))
        self.assertTrue(isinstance(dic, Iterable))

    def test_iterator_1(self):
        """
        create an Iterator from iter(Iterable)
        """
        ite = iter(lst)
        self.assertTrue(isinstance(ite, Iterator))


unittest.main()

