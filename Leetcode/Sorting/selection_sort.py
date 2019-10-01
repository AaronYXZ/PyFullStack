class SelectionSort():
    def sort(self, data):
        if data is None:
            raise TypeError("data cannot be None")
        if len(data) < 2:
            return data
        for i in range(len(data)-1):
            min_index = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_index]:
                    min_index = j
            if data[min_index] < data[i]:
                data[i], data[min_index] = data[min_index], data[i]
        return data

import unittest
class TestSelectionSort(unittest.TestCase):
    def test1(self):
        return None

    def test2(self):
        lst = [1,2,5,3,4]
        sorted = SelectionSort().sort(lst)
        self.assertEqual(sorted, [1,2,3,4,5])
