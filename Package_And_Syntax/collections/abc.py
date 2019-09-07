from collections.abc import Iterable, Iterator, Generator, Collection, Hashable
import unittest

class test_collections_abc(unittest.TestCase):
    def test1(self):
        """
        check if range is Iterable / Iterator
        """
        a = range(10)
        self.assertTrue(isinstance(a, Iterable), "should be Iterable")
        self.assertFalse(isinstance(a, Iterator), "should not be Iterator")
        self.assertFalse(isinstance(a, Generator))
    def test2(self):
        """
        check if list is Collection / Hashable
        """
        b = list((1,2,3))
        self.assertTrue(isinstance(b, Collection))
        self.assertFalse(isinstance(b, Hashable))

unittest.main()