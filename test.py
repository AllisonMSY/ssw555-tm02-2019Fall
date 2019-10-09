import unittest
import project4

class test(unittest.TestCase):

    def test_story01(self):
        p1 = project4.Person("I01T", "testPerson1", "M", "24 DEC 1969", "", "", "")
        self.assertEqual(p1.birth_before_current_date(), True)
        p2 = project4.Person("I02T", "testPerson2", "F", "9 MAR 2027", "", "", "")
        self.assertEqual(p2.birth_before_current_date()[0], False)
        p3 = project4.Person("I03T", "testPerson3", "F", "24 DEC 1980", "25 OCT 1999", "", "")
        self.assertEqual(p3.death_before_current_date(), True)
        p4 = project4.Person("I04T", "testPerson4", "M", "24 DEC 1990", "6 JAN 2039", "", "")
        self.assertEqual(p4.death_before_current_date()[0], False)
        p5 = project4.Person("I05T", "testPerson5", "M", "15 APR 1956", "", "", "")
        p6 = project4.Person("I06T", "testPerson6", "F", "27 JUN 1960", "", "", "")
        f1 = project4.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "19 NOV 1990", "20 JAN 2004", "I05T", "I06T"
        self.assertTrue(f1.marry_before_current_date())
        self.assertTrue(f1.divorce_before_current_date())
        p7 = project4.Person("I07T", "testPerson7", "F", "25 MAR 2001", "", "", "")
        p8 = project4.Person("I08T", "testPerson8", "M", "17 MAY 2002", "", "", "")
        f2 = project4.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "10 OCT 2027", "14 FEB 2029", "I08T", "I07T"
        self.assertFalse(f2.marry_before_current_date()[0])
        self.assertFalse(f2.divorce_before_current_date()[0])

    def test_story02(self):
        p1 = project4.Person("I01T", "testPerson1", "F", "15 APR 1990", "", "", "")
        p2 = project4.Person("I02T", "testPerson2", "M", "27 JUN 1987", "", "", "")
        personList = [p1, p2]
        f1 = project4.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "9 MAR 1950", "", "I01T", "I02T"
        f2 = project4.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "9 JUL 2015", "11 JUN 2018", "I01T", "I02T"
        family = [f1, f2]
        self.assertFalse(p1.birth_before_marriage(family)[0])
        self.assertTrue(p2.birth_before_marriage(family))

    def test_story03(self):
        p = project4.Person("I03T", "P03", "F", "4 MAR 2000",
                            "4 MAR 2010", "", "")
        self.assertEqual(p.birth_before_death(), True)
        p = project4.Person("I03T", "P03", "F", "4 MAR 2010", "4 MAR 2000",
                            "", "")
        self.assertEqual(p.birth_before_death()[0], False)

    def test_story04(self):
        f = project4.Family("F04T")
        f.Married, f.Divorced = "4 MAR 2000", "4 MAR 2010"
        self.assertEqual(f.marriage_before_divorce(), True)
        f.Married, f.Divorced = "4 MAR 2010", "4 MAR 2000"
        self.assertEqual(f.marriage_before_divorce()[0], False)

    def test_story05(self):
        p1 = project4.Person("I01T", "testName1", "M", "2 SEP 1741", "21 DEC 1973", "", "")
        p2 = project4.Person("I02T", "testName2", "F", "19 FEB 1746", "", "", "")

        personList = [p1, p2]

        f1 = project4.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "21 DEC 1973", "21 DEC 1973", "I01T", "I02T"

        self.assertFalse(f1.parents_not_marry_before_they_dead(personList)[0])

        f2 = project4.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "21 DEC 1966", "21 DEC 1969", "I01T", "I02T"

        self.assertTrue(f2.parents_not_marry_before_they_dead(personList))


    def test_story06(self):
        p1 = project4.Person("I01T", "testName1", "M", "2 SEP 1741", "21 DEC 1973", "", "")
        p2 = project4.Person("I02T", "testName2", "F", "19 FEB 1746", "", "", "")

        personList = [p1, p2]

        f1 = project4.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "21 DEC 1973", "21 DEC 1973", "I01T", "I02T"

        self.assertFalse(f1.parents_not_divorce_before_they_dead(personList)[0])

        f2 = project4.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "21 DEC 1966", "21 DEC 1969", "I01T", "I02T"

        self.assertTrue(f2.parents_not_divorce_before_they_dead(personList))
        
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
