import unittest
import project4

class test(unittest.TestCase):

    def story08(self):
        p1 = project4.Person(I01, dadasaf,M,'DATE 2 SEP 1741','DATE 21 DEC 1973','','')
        p2 = project4.Person(I02,dadva,F,'DATE 21 DEC 1943','','','')
        self.assertFalse(p1.less_than_150())
        self.assertTrue(p2.less_than_150())



if __name__ == '__main__':
    unittest.main()