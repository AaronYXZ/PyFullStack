import unittest
from Dict import Dict

class TestDict(unittest.TestCase):
    """
    https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/00143191629979802b566644aa84656b50cd484ec4a7838000

    """
    def test_init(self):
        d = Dict(a = 1, b = "test")
        self.assertEqual(d.a, 1)
        self.assertEqual(d['b'], "test")
        self.assertTrue(isinstance(d, Dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = "value"
        self.assertEqual(d['key'], 'value')
        self.assertTrue('key' in d)

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            value = d["empty"]
    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            value = d.empty



if __name__ == '__main__':
    unittest.main()