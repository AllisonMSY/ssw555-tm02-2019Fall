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
    def test_story08(self):
        p1 = project4.Person("I01","adasasfa","F","21 DEC 1993","","","")
        p2 = project4.Person("I02","faasda","F","21 DEC 1973","","","")
        personObj1 = []
        personObj1.append(p1)
        personObj2 = []
        personObj2.append(p2)
        f1 = project4.Family("F00")
        f1.Married = "21 DEC 1983"
        f1.Children.append("I01")
        f1.Children.append("I02")
        self.assertTrue(f1.child_not_birth_before_parents_marriage(personObj1))
        self.assertFalse(f1.child_not_birth_before_parents_marriage(personObj2)[0])


if __name__ == '__main__':
    unittest.main()