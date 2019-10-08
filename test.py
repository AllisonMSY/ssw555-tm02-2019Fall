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

    def test_story03(self):
        p = project4.Person("I03T", "P03", "F", "4 MAR 2000",
                            "4 MAR 2010", "", "")
        self.assertEqual(p.birth_before_death(), True)
        p = project4.Person("I03T", "P03", "F", "4 MAR 2010", "4 MAR 2000",
                            "", "")
        self.assertEqual(p.birth_before_death()[0], False)

if __name__ == '__main__':
    unittest.main()
