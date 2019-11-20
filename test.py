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

    def test_story12(self):
        p1 = project.Person("I01")
        p1.name, p1.gender, p1.BirthDate = "hhh", "M", "26 MAY 1776"
        p2 = project.Person("I02")
        p2.name, p2.gender, p2.BirthDate = "www", "F", "8 FEB 1780"
        p3 = project.Person("I03")
        p3.name, p3.gender, p3.BirthDate = "ccc", "F", "14 JUL 2019"
        p4 = project.Person("I04")
        p4.name, p4.gender, p4.BirthDate = "kkk", "M", "10 JAN 1990"
        p5 = project.Person("I05")
        p5.name, p5.gender, p5.BirthDate = "lll", "F", "23 FEB 1990"
        p6 = project.Person("I06")
        p6.name, p6.gender, p6.BirthDate = "ttt", "M", "24 DEC 2018"

        personList1 = [p1, p2, p3]
        personList2 = [p4, p5, p6]

        f1 = project.Family("FFF")
        f1.HusbandID, f1.WifeID = "I01", "I02"
        f1.Children.append("I03")
        f2 = project.Family("FFF01")
        f2.HusbandID, f2.WifeID = "I04", "I05"
        f2.Children.append("I06")
        self.assertFalse(f1.Parents_not_too_old(personList1)[0])
        self.assertTrue(f2.Parents_not_too_old(personList2))

    def test_story14(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p5 = project.Person("I05T")
        p6 = project.Person("I06T")
        p7 = project.Person("I07T")
        plist = [p1,p2,p3,p4,p5,p6,p7]
        for p in plist:
            p.BirthDate = "21 NOV 2000"
        f1 = project.Family("F01")
        f2 = project.Family("F02")
        f1.Children.extend(["I01T","I02T","I03T","I04T","I05T","I06T","I07T"])
        f2.Children.extend(["I01T","I02T"])
        self.assertTrue(f2.multiple_birth_less_than_5(plist))
        self.assertFalse(f1.multiple_birth_less_than_5(plist)[0])

    def test_story15(self):
        f1 = project.Family("F01")
        f2 = project.Family("F02")
        f1.HusbandID, f1.WifeID = "I01T", "I02T"
        f1.Children.append("I05T")
        f2.HusbandID, f2.WifeID = "I03T", "I04T"
        f2.Children.extend(["I06T","I07T","I08T","I09T","I10T","I11T","I12T","I13T","I14T","I15T","I16T","I17T","I18T","I19T","I20T","I21T"])
        self.assertTrue(f1.fewer_than_15_siblings())
        self.assertFalse(f2.fewer_than_15_siblings()[0])

    def test_story16(self):
        p1 = project.Person("I01")
        p1.name, p1.gender = "Tom /Davis/", "M"
        p2 = project.Person("I02")
        p2.name, p2.gender = "Lily /Davis/", "F"
        p3 = project.Person("I03")
        p3.name, p3.gender = "Jerry /Miller/", "M"
        p4 = project.Person("I04")
        p4.name, p4.gender = "Mike /Miller/", "M"
        p5 = project.Person("I05")
        p5.name, p5.gender = "Sue /Miller/", "F"
        p6 = project.Person("I06")
        p6.name, p6.gender = "Alex /Miller/", "M"

        personList1 = [p1, p2, p3]
        personList2 = [p4, p5, p6]

        f1 = project.Family("FFF")
        f1.HusbandID, f1.WifeID = "I01", "I02"
        f1.Children.append("I03")
        f2 = project.Family("FFF01")
        f2.HusbandID, f2.WifeID = "I04", "I05"
        f2.Children.append("I06")
        self.assertFalse(f1.Male_last_names(personList1)[0])
        self.assertTrue(f2.Male_last_names(personList2))

    def test_story21(self):
        f1 = project.Family("F01")
        f2 = project.Family("F02")
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p1.name, p1.gender = "Tom", "M"
        p2.name, p2.gender = "Lisa", "F"
        p3.name, p3.gender = "Ross", "F"
        p4.name, p4.gender = "Emily", "M"
        familyList1 = [p1, p2]
        familyList2 = [p3, p4]
        f1.HusbandID, f1.WifeID = "I01T", "I02T"
        f2.HusbandID, f2.WifeID = "I03T", "I04T"
        self.assertTrue(f1.correct_gender_for_role(familyList1))
        self.assertFalse(f2.correct_gender_for_role(familyList2)[0])

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

    def test_story28(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate, p1.FID_spouse = "John /ad/", "M", "14 Jan 1980", "2 MAR 2013", ["F00"]
        p2.name, p2.gender, p2.BirthDate, p2.DeathDate, p2.FID_spouse = "Ali /ad/", "F", "4 MAY 1984", "12 DEC 2015", ["F00"]
        p3.name, p3.gender, p3.BirthDate, p3.FID_child = "Zed /ad/", "F", "5 FEB 2018", ["F00"]
        f1 = project.Family("F00")
        f1.HusbandID, f1.WifeID = "I01T", "I02T"
        f1.Children.append("I03T")
        personList = [p1, p2, p3]
        familyList = [f1]
        res = project.list_all_orphans(familyList, personList)
        self.assertEqual([p3], res)

    def test_story29(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate, p1.FID_spouse = "John /ad/", "M", "14 Jan 1980", "2 MAR 2013", ["F00"]
        p2.name, p2.gender, p2.BirthDate, p2.DeathDate, p2.FID_spouse = "Ali /ad/", "F", "4 MAY 1984", "12 DEC 2015", ["F00"]
        p3.name, p3.gender, p3.BirthDate, p3.FID_child = "Zed /ad/", "F", "5 FEB 2018", ["F00"]
        personList = [p1, p2, p3]
        res = p1.list_deceased_individuals(personList)
        self.assertEqual([p1, p2], res)

    def test_story30(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p5 = project.Person("I04T")
        p1.name,p1.BirthDate,p1.FID_spouse = "A", "21 JUL 1973", ["I02T"]
        p2.name,p2.BirthDate,p2.FID_spouse = "B", "21 JUL 1983", ["I01T"]
        p3.name,p3.BirthDate = "C", "21 JUL 1983",
        p4.name,p4.BirthDate,p4.FID_spouse = "D", "21 JUL 1993",["I05T"]
        p5.name,p5.BirthDate,p5.DeathDate,p5.name = "E","21 JUL 1993","21 JUL 2003",["I04T"]
        personList1 = [p1,p2,p3,p4,p5]
        personList2 = [p1,p2,p3]
        self.assertEqual(project.Person.list_living_married(personList1),[p1,p2,p4])
        self.assertEqual(project.Person.list_living_married(personList2),[p1,p2])

    def test_story31(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p5 = project.Person("I04T")
        p1.name,p1.BirthDate = "A", "21 JUL 1973"
        p2.name,p2.BirthDate = "B", "21 JUL 1983"
        p3.name,p3.BirthDate,p3.DeathDate = "C", "21 JUL 1983", "21 JUL 2013"
        p4.name,p4.BirthDate,p4.FID_spouse = "D", "21 JUL 1983",["I05T"]
        p5.name,p5.BirthDate,p5.DeathDate,p5.name = "E","21 JUL 1983","21 JUL 2003",["I04T"]
        personList1 = [p1,p2,p3,p4,p5]
        personList2 = [p2,p3,p4,p5]
        self.assertEqual(project.Person.list_living_single(personList1),[p1,p2])
        self.assertEqual(project.Person.list_living_single(personList2),[p2])

    def test_story32(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate, p1.FID_spouse = "John /ad/", "M", "4 MAY 1984", "2 MAR 2013", ["F00"]
        p2.name, p2.gender, p2.BirthDate, p2.DeathDate, p2.FID_spouse = "Ali /ad/", "F", "4 MAY 1984", "12 DEC 2015", ["F00"]
        p3.name, p3.gender, p3.BirthDate, p3.FID_child = "Zed /ad/", "F", "5 FEB 2018", ["F00"]
        personList = [p1, p2, p3]
        res = p1.list_multiple_births(personList)
        self.assertEqual([p1, p2], res)

    def test_story33(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p5 = project.Person("I05T")
        p1.name, p1.gender, p1.BirthDate, p1.DeathDate, p1.FID_spouse = "John /ad/", "M", "14 Jan 1980", "2 MAR 2013", ["F00"]
        p2.name, p2.gender, p2.BirthDate, p2.DeathDate, p2.FID_spouse = "Ali /ad/", "F", "4 MAY 1984", "12 DEC 2015", ["F00"]
        p3.name, p3.gender, p3.BirthDate, p3.FID_child = "Zed /ad/", "F", "5 FEB 2018", ["F00"]
        p4.name, p4.gender, p4.BirthDate, p4.FID_child = "Tom /ad/", "F", "5 FEB 2003", ["F00"]
        p5.name, p5.gender, p5.BirthDate, p5.FID_child = "Sue /ad/", "F", "5 FEB 2007", ["F00"]
        f1 = project.Family("F00")
        f1.HusbandID, f1.WifeID = "I01T", "I02T"
        f1.Children.append("I03T")
        f1.Children.append("I04T")
        f1.Children.append("I05T")
        personList = [p1, p2, p3, p4, p5]
        familyList = [f1]
        res = project.list_siblings_by_age("F00", familyList, personList)
        self.assertEqual([p4,p5,p3], res)

    def test_story35(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.BirthDate = "A", "31 Oct 2019"
        p2.name, p2.BirthDate = "B", "21 JUL 1983"
        self.assertEqual(project.Person.list_recent_birth([p1, p2, p3], date(2019, 11, 2)), [p1])

    def test_story36(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p1.name, p1.DeathDate, p1.BirthDate = "A", "31 Oct 2019", "31 Oct 2000"
        p2.name, p2.DeathDate, p2.BirthDate = "B", "21 JUL 1983", "21 JUL 1940"
        self.assertEqual(project.Person.list_recent_death([p1, p2, p3], date(2019, 11, 2)), [p1])

    def test_story37(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        p1.name, p1.DeathDate, p1.BirthDate = "A", "13 NOV 2019", "31 Oct 1980"
        p2.name, p2.BirthDate = "B",  "21 JUL 1940"
        p3.name, p3.DeathDate, p3.BirthDate = "A", "13 NOV 2019", "31 Oct 2000"
        p4.name, p4.BirthDate = "B",  "21 JUL 2018"
        f1 = project.Family("F00")
        f2 = project.Family("F01")
        f3 = project.Family("F00")
        f1.HusbandID,f1.WifeID = "I01T","I02T"
        f1.Children.append("I04T")
        f2.WifeID,f2.HusbandID = "I01T","I02T"
        f3.HusbandID,f3.WifeID = "I01T","I03T"
        f3.Children.append("I04T")
        plist = [p1,p2,p3,p4]
        self.assertEqual(f1.get_survivor_in_the_family(plist)[0],[p1])
        self.assertEqual(f1.get_survivor_in_the_family(plist)[1],[p2,p4])
        self.assertEqual(f2.get_survivor_in_the_family(plist)[0],[p1])
        self.assertEqual(f2.get_survivor_in_the_family(plist)[1],[p2])
        self.assertEqual(f3.get_survivor_in_the_family(plist)[0],[p1,p3])
        self.assertEqual(f3.get_survivor_in_the_family(plist)[1],[p4])


    def test_story38(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        # birthday is in the middle of a year
        p1.name, p1.BirthDate = "Alice", "21 JUL 1973"
        # birthday is at the beginning of a year
        p2.name, p2.BirthDate = "Bob", "21 JAN 1993"
        # birthday is at the beginning of a year but already dead
        p3.name, p3.BirthDate, p3.DeathDate = "Sue", "12 JAN 1993", "15 JUL 2017"
        # birthday is in the middle of a year but already dead
        p4.name, p4.BirthDate, p4.DeathDate = "Alex", "12 JAN 1992", "15 JUL 2016"
        personList = [p1, p2, p3, p4]
        today1 = date(2019, 12, 31)  # this last day of a year.
        today2 = date(2019, 6, 30)  # this last day of a year.
        self.assertEqual(
            [p2], project.Person.list_upcoming_birthdays_from_date(personList, today1))
        self.assertEqual(
            [p1], project.Person.list_upcoming_birthdays_from_date(personList, today2))

    def test_story39(self):
        p1 = project.Person("I01T")
        p2 = project.Person("I02T")
        p3 = project.Person("I03T")
        p4 = project.Person("I04T")
        # birthday is in the middle of a year
        p1.name, p1.BirthDate = "Alice", "21 JUL 1973"
        # birthday is at the beginning of a year
        p2.name, p2.BirthDate = "Bob", "21 JAN 1993"
        # birthday is at the beginning of a year but already dead
        p3.name, p3.BirthDate, p3.DeathDate = "Sue", "12 JAN 1993", "15 JUL 2017"
        # birthday is in the middle of a year but already dead
        p4.name, p4.BirthDate, p4.DeathDate = "Alex", "12 JAN 1992", "15 JUL 2016"
        f1 = project.Family("F00T")
        f2 = project.Family("F01T")
        f3 = project.Family("F02T")

        f1.HusbandID, f1.WifeID, f1.Married = "I01T", "I02T", "12 JAN 2015"
        f2.HusbandID, f2.WifeID, f2.Married, f2.Divorced = "I01T", "I02T", "12 JAN 2015", "12 MAR 2017"  # divorced
        f3.HusbandID, f3.WifeID, f3.Married = "I03T", "I04T", "12 JAN 2015"  # both dead
        today = date(2019, 12, 31)
        personList = [p1, p2, p3, p4]
        familyList = [f1, f2, f3]

        self.assertEqual([f1], project.Family.list_upcoming_anniversaries_from_date(
            familyList, personList, today))


if __name__ == '__main__':
    unittest.main()
