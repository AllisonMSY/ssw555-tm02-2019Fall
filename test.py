import unittest
import project4

class test(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
