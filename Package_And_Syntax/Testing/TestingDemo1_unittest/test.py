import unittest

from my_sum.sumFunc import sum2

class TestSum(unittest.TestCase):

    def test_list_int(self):
        """
        Test that it can sum a list of integers
        :return:
        """
        data = [1,2,3]
        result = sum2(data)
        self.assertEqual(result, 6)


if __name__ == '__main__':
    unittest.main()