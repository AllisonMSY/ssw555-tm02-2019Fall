import unittest
import project4

class test(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    def test_story07(self):
        p1 = project4.Person("I01","adasi","F","21 DEC 1773","21 DEC 1973","","")
        p2 = project4.Person("I02","adasi","F","21 DEC 1973","","","")
        self.assertTrue(p2.less_than_150())
        self.assertFalse(p1.less_than_150()[0])


if __name__ == '__main__':
    unittest.main()