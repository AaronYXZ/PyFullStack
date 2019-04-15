import unittest


# def test_sum():
#     assert sum([1, 2, 3]) == 6, "Should be 6"
#
# def test_sum_tuple():
#     assert sum((1, 2, 2)) == 6, "Should be 6"
#
# if __name__ == "__main__":
#     test_sum()
#     test_sum_tuple()
#     print("Everything passed")


# To convert the earlier example to a unittest test case, you would have to:
#
# Import unittest from the standard library
# Create a class called TestSum that inherits from the TestCase class
# Convert the test functions into methods by adding self as the first argument
# Change the assertions to use the self.assertEqual() method on the TestCase class
# Change the command-line entry point to call unittest.main()

class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()