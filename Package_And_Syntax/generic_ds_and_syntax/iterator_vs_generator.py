from collections.abc import Iterator, Generator, Iterable
import unittest

def generator_count_down(num):
    print("Starting")
    while num > 0:
        yield num
        num -= 1

class test_iterator_generator(unittest.TestCase):

    def test_iterator_generator(self):
        self.assertTrue(issubclass(Generator, Iterator))
        self.assertFalse(issubclass(Iterator, Generator))
        self.assertTrue(issubclass(Generator, Iterable))

    def test_generator(self):
        g = generator_count_down(5)
        self.assertTrue(isinstance(g, Generator))
        g2 = (x for x in range(5))
        self.assertTrue(isinstance(g2, Generator))

if __name__ == '__main__':
    unittest.main()