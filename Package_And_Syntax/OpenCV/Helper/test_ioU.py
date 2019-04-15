from unittest import TestCase, main
from Eval import IoU



Reframe1 = [3, 1, 10, 9]
GTframe1 = [3, 1, 10, 9]
GTframe2 = [7, 4, 15, 14]


class TestIoU(TestCase):

    def test_perfectMatch(self):
        self.assertEqual(IoU(Reframe1, GTframe1), 1.0, "Should be 1")
    def test_partialMatch(self):
        self.assertEqual(IoU(Reframe1, GTframe2), 15.0 / (56 + 80 - 15), "NOT CORRECT")


if __name__ == '__main__':
    main()
