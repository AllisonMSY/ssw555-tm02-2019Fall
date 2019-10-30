import unittest
import project
import readFile
from datetime import date


class test(unittest.TestCase):

    def test_readFile(self):
        fileName = "./testFile/travis_test.txt"
        res = readFile.readGCFile(fileName)
        expectResult = [[0, 'INDI', 'I00', 4], [1, 'NAME', 'Ulises /Bubb/', 5], [1, 'SEX', 'M', 6], [1, 'BIRT', '', 8], [2, 'DATE', '2 SEP 1941', 9], [1, 'DEAT', '', 10], [2, 'DATE', '21 DEC 1973', 11], [1, 'FAMS',
                                                                                                                                                                                                            'F00', 12], [0, 'FAM', 'F00', 16], [1, 'MARR', '', 17], [2, 'DATE', '14 FEB 1966', 18], [1, 'HUSB', 'I00', 19], [1, 'WIFE', 'I01', 20], [1, 'CHIL', 'I04', 21], [1, 'CHIL', 'I05', 22], [1, 'CHIL', 'I06', 23]]
        self.assertEqual(res, expectResult)

    def test_story01(self):
        p1 = project.Person("I01T")
        p1.name, p1.gender, p1.BirthDate = "testPerson1", "M", "24 DEC 1969"
        self.assertEqual(p1.birth_before_current_date(), True)
        p2 = project.Person("I02T")
        p2.name, p2.gender, p2.BirthDate = "testPerson2", "F", "9 MAR 2027"
        self.assertEqual(p2.birth_before_current_date()[0], False)
        p3 = project.Person("I03T")
        p3.name, p3.gender, p3.BirthDate, p3.DeathDate = "testPerson3", "F", "24 DEC 1980", "25 OCT 1999"
        self.assertEqual(p3.death_before_current_date(), True)
        p4 = project.Person("I04T")
        p4.name, p4.gender, p4.BirthDate, p4.DeathDate = "testPerson4", "M", "24 DEC 1990", "6 JAN 2039"
        self.assertEqual(p4.death_before_current_date()[0], False)
        # p5 = project.Person("I05T", "testPerson5", "M", "15 APR 1956", "NA", "NA", "NA")
        # p6 = project.Person("I06T", "testPerson6", "F", "27 JUN 1960", "NA", "NA", "NA")
        f1 = project.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "19 NOV 1990", "20 JAN 2004", "I05T", "I06T"
        self.assertTrue(f1.marry_before_current_date())
        self.assertTrue(f1.divorce_before_current_date())
        # p7 = project.Person("I07T", "testPerson7", "F", "25 MAR 2001", "NA", "NA", "NA")
        # p8 = project.Person("I08T", "testPerson8", "M", "17 MAY 2002", "NA", "NA", "NA")
        f2 = project.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "10 OCT 2027", "14 FEB 2029", "I08T", "I07T"
        self.assertFalse(f2.marry_before_current_date()[0])
        self.assertFalse(f2.divorce_before_current_date()[0])

    def test_story02(self):
        p1 = project.Person("I01T")
        p1.name, p1.gender, p1.BirthDate = "testPerson1", "F", "15 APR 1990"
        p2 = project.Person("I02T")
        p2.name, p2.gender, p2.BirthDate = "testPerson2", "M", "27 JUN 1987"
        # personList = [p1, p2]
        f1 = project.Family("F01T")
        f1.Married, f1.HusbandID, f1.WifeID = "9 MAR 1950", "I01T", "I02T"
        f2 = project.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "9 JUL 2015", "11 JUN 2018", "I01T", "I02T"
        family = [f1, f2]
        self.assertFalse(p1.birth_before_marriage(family)[0])
        self.assertTrue(p2.birth_before_marriage(family))

    def test_story03(self):
        p = project.Person("I03T")
        p.name, p.gender, p.BirthDate, p.DeathDate = "P03", "F", "4 MAR 2000", "4 MAR 2010"
        self.assertEqual(p.birth_before_death(), True)
        p = project.Person("I03T")
        p.name, p.gender, p.BirthDate, p.DeathDate = "P03", "F", "4 MAR 2010", "4 MAR 2000"
        self.assertEqual(p.birth_before_death()[0], False)

    def test_story04(self):
        f = project.Family("F04T")
        f.Married, f.Divorced = "4 MAR 2000", "4 MAR 2010"
        self.assertEqual(f.marriage_before_divorce(), True)
        f.Married, f.Divorced = "4 MAR 2010", "4 MAR 2000"
        self.assertEqual(f.marriage_before_divorce()[0], False)

    def test_story05(self):
        p1 = project.Person("I01T")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate = "testName1", "M", "2 SEP 1741", "21 DEC 1973"
        p2 = project.Person("I02T")
        p2.name, p2.gender, p2.BirthDate = "testName2", "F", "19 FEB 1746"

        personList = [p1, p2]

        f1 = project.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "21 DEC 1973", "21 DEC 1973", "I01T", "I02T"

        self.assertFalse(f1.parents_not_marry_before_they_dead(personList)[0])

        f2 = project.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "21 DEC 1966", "21 DEC 1969", "I01T", "I02T"

        self.assertTrue(f2.parents_not_marry_before_they_dead(personList))

    def test_story06(self):
        p1 = project.Person("I01T")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate = "testName1", "M", "2 SEP 1741", "21 DEC 1973"
        p2 = project.Person("I02T")
        p2.name, p2.gender, p2.BirthDate = "testName2", "F", "19 FEB 1746"

        personList = [p1, p2]

        f1 = project.Family("F01T")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "21 DEC 1973", "21 DEC 1973", "I01T", "I02T"

        self.assertFalse(
            f1.parents_not_divorce_before_they_dead(personList)[0])

        f2 = project.Family("F02T")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "21 DEC 1966", "21 DEC 1969", "I01T", "I02T"

        self.assertTrue(f2.parents_not_divorce_before_they_dead(personList))

    def test_story07(self):
        p1 = project.Person("I01")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate = "adasi", "F", "21 DEC 1773", "21 DEC 1973"
        p2 = project.Person("I02")
        p2.name, p2.gender, p2.BirthDate = "adasi", "F", "21 DEC 1973"
        self.assertTrue(p2.less_than_150())
        self.assertFalse(p1.less_than_150()[0])

    def test_story08(self):
        p1 = project.Person("I01")
        p1.name, p1.gender, p1.BirthDate = "adasasfa", "F", "21 DEC 1993"

        p2 = project.Person("I02")
        p2.name, p2.gender, p2.BirthDate = "faasda", "F", "21 DEC 1973"

        personObj1 = []
        personObj1.append(p1)
        personObj2 = []
        personObj2.append(p2)
        f1 = project.Family("F00")
        f1.Married = "21 DEC 1983"
        f1.Children.append("I01")
        f1.Children.append("I02")
        self.assertTrue(f1.child_not_birth_before_parents_marriage(personObj1))
        self.assertFalse(
            f1.child_not_birth_before_parents_marriage(personObj2)[0])

    def test_story09(self):
        p1 = project.Person("I01")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate = "hhh", "M", "26 MAY 1976", "20 JAN 2010"
        p2 = project.Person("I02")
        p2.name, p2.gender, p2.BirthDate, p2.DeathDate = "www", "F", "8 FEB 1980", "27 JUN 2014"
        p3 = project.Person("I03")
        p3.name, p3.gender, p3.BirthDate = "ccc", "F", "14 JUL 2017"
        p4 = project.Person("I04")
        p4.name, p4.gender, p4.BirthDate, p4.DeathDate = "kkk", "M", "10 JAN 1970", "4 MAY 2010"
        p5 = project.Person("I05")
        p5.name, p5.gender, p5.BirthDate, p5.DeathDate = "lll", "F", "23 FEB 1977", "4 MAY 2010"
        p6 = project.Person("I06")
        p6.name, p6.gender, p6.BirthDate = "ttt", "M", "24 DEC 2005"

        personList1 = [p1, p2, p3]
        personList2 = [p4, p5, p6]

        f1 = project.Family("FFF")
        f1.Married, f1.Divorced, f1.HusbandID, f1.WifeID = "11 JAN 2010", "", "I01", "I02"
        f1.Children.append("I03")
        f2 = project.Family("FFF01")
        f2.Married, f2.Divorced, f2.HusbandID, f2.WifeID = "20 APR 2000", "", "I04", "I05"
        f2.Children.append("I06")
        self.assertFalse(f1.birth_before_death_of_parents(personList1)[0])
        self.assertTrue(f2.birth_before_death_of_parents(personList2))

    def test_story10(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.gender, p1.BirthDate = "adasd", "M", "21 DEC 1973"
        p2.name, p2.gender, p2.BirthDate = "dacadaw", "M", "21 SEP 1993"
        p3.name, p3.gender, p3.BirthDate = "badacaaq", "F", "21 DEC 1983"
        personList1 = [p1, p3]
        personList2 = [p2, p3]
        f1 = project.Family("F00T")
        f2 = project.Family("F01T")
        f1.Married, f1.HusbandID, f1.WifeID = "21 NOV 2000", "I01T", "I03T"
        f2.Married, f2.HusbandID, f2.WifeID = "21 DEC 2000", "I02T", "I03T"
        self.assertTrue(f1.marriage_after_14(personList1))
        self.assertFalse(f2.marriage_after_14(personList2)[0])

    def test_story22(self):
        p1 = project.Person("I01")
        p2 = project.Person("I01")
        p3 = project.Person("I02")
        personList1 = [p1, p2]
        personList2 = [p2, p3]
        f1 = project.Family("F00")
        f2 = project.Family("F00")
        f3 = project.Family("F01")
        familyList1 = [f1, f2]
        familyList2 = [f2, f3]
        self.assertTrue(f3.unique_family_id(familyList2))
        self.assertTrue(p3.unique_person_id(personList2))
        self.assertFalse(p1.unique_person_id(personList1)[0])
        self.assertFalse(f1.unique_family_id(familyList1)[0])

    def test_story23(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.BirthDate = "Alice", "21 DEC 1973"
        p2.name, p2.BirthDate = "Bob", "21 SEP 1993"
        p3.name, p3.BirthDate = "Bob", "21 SEP 1993"
        personList1 = [p1, p3]
        personList2 = [p2, p3]
        self.assertTrue(p1.unique_name_and_birth_date(personList1))
        self.assertFalse(p2.unique_name_and_birth_date(personList2)[0])

    def test_story24(self):
        f1 = project.Family("F001T")
        f2 = project.Family("F001T")
        f3 = project.Family("F001T")
        f1.HusandName, f1.WifeName, f1.Married = "Bob", "Alice", "21 DEC 1973"
        f2.HusandName, f2.WifeName, f2.Married = "Bob", "Ali", "21 DEC 1973"
        f3.HusandName, f3.WifeName, f3.Married = "Bob", "Ali", "21 DEC 1973"
        family1, family2 = [f1, f2], [f2, f3]
        self.assertTrue(f1.unique_families_by_spouses(family1))
        self.assertFalse(f1.unique_families_by_spouses(family2)[0])

    def test_story25(self):
        f1 = project.Family("F00")
        f2 = project.Family("F01")
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p1.name, p1.gender = "John /ad/", "M"
        p2.name, p2.gender = "Ali /ad/", "F"
        p3.name, p3.gender = "Zed /ad/", "F"
        p4.name, p4.gender = "John /ad/", "M"
        personList1 = [p1, p2, p3]
        personList2 = [p1, p2, p4]
        f1.HusbandID, f1.WifeID = "I01T", "I02T"
        f1.Children.append("I03T")
        f2.HusbandID, f2.WifeID = "I01T", "I02T"
        f2.Children.append("I04T")
        self.assertTrue(f1.unique_first_name_in_family(personList1))
        self.assertFalse(f2.unique_first_name_in_family(personList2)[0])

    def test_story38(self):
        pass

    def test_story39(self):
        pass


if __name__ == '__main__':
    unittest.main()
