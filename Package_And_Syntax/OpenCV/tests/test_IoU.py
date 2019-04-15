import unittest
from .Helper.Eval import IoU

class TestIoU(unittest.TestCase):
    Reframe1 = [1, 3, 10, 9]
    GTframe1 = [1,3,10,9]

    def test_perfectMatch(self):
        self.assertEqual(IoU(Reframe1, GTframe1), "Should be 1")

    # def test_sum_tuple(self):
    #     self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()


