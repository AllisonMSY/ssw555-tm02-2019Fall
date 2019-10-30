from prettytable import PrettyTable
from datetime import date
import datetime


def printPeoplePrettyTable(PersonList):
    personTable = PrettyTable()
    personTable.field_names = ["ID", "Name", "Gender", "Birthday",
                               "Age", "Alive", "Death", "Child", "Spouse"]

    for one in PersonList:
        child = "NA"
        spouse = "NA"
        death = "NA"
        alive = "Y"
        born = datetime.datetime.strptime(one.BirthDate, "%d %b %Y").date()
        today = date.today()
        age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))

        if one.FID_child:
            child = one.FID_child
        if one.FID_spouse:
            spouse = one.FID_spouse
        if one.DeathDate != "NA":
            alive = "N"
            death = one.DeathDate
            today = datetime.datetime.strptime(
                one.DeathDate, "%d %b %Y").date()
            age = today.year - born.year - \
                ((today.month, today.day) < (born.month, born.day))

        personTable.add_row([one.INDI_id, one.name, one.gender,
                             one.BirthDate, age, alive, death, child, spouse])

    print(personTable)


def printFamilyPrettyTable(FamilyList, PersonList):
    familyTable = PrettyTable()
    familyTable.field_names = ["ID", "Married", "Divorced", "Husband ID",
                               "Husband Name", "Wife ID", "Wife Name",
                               "Children"]
    for one in FamilyList:
        Children = "NA"
        if one.Children:
            Children = one.Children
        for oneP in PersonList:
            if oneP.INDI_id == one.HusbandID:
                one.HusbandName = oneP.name
            if oneP.INDI_id == one.WifeID:
                one.WifeName = oneP.name

        familyTable.add_row(
            [one.ID, one.Married, one.Divorced, one.HusbandID, one.HusbandName,
             one.WifeID, one.WifeName, Children])

    print(familyTable)
