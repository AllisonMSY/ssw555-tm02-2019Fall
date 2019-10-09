from prettytable import PrettyTable
from datetime import date
import datetime

fileName = "./test_project4.txt"

_TAGLIST0_1 = ['HEAD', 'TRLR', 'NOTE']
_TAGLIST0_2 = ['INDI', 'FAM']
_TAGLIST1_INDI = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
_TAGLIST1_FAM = ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
_TAGLIST2 = ['DATE']


def get_age(person):
    born = datetime.datetime.strptime(person.BirthDate, "%d %b %Y").date()
    if person.DeathDate != "":
        today = datetime.datetime.strptime(person.DeathDate, "%d %b %Y").date()
        age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))
    else:
        today = date.today()
        age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))
    return age



class Person:
    def __init__(self, INDI_id, name, gender, BirthDate,
                 DeathDate, FID_child, FID_spouse):
        self.INDI_id = INDI_id
        self.name = name
        self.gender = gender
        self.BirthDate = BirthDate
        self.DeathDate = DeathDate
        self.FID_child = FID_child
        self.FID_spouse = FID_spouse

    def birth_before_current_date(self):
        # Story 01 Birth
        born = datetime.datetime.strptime(self.BirthDate, "%d %b %Y").date()
        if born < date.today():
            return True
        reason = "ERROR: INDIVIDUAL: US01: LINE#: {}: Birthday {} occurs in the future"
        return False, reason.format(self.INDI_id, self.BirthDate)

    def death_before_current_date(self):
        # Story 01 Death
        if self.DeathDate == '':
            return True
        death = datetime.datetime.strptime(self.DeathDate, "%d %b %Y").date()
        if death < date.today():
            return True
        reason = "ERROR: INDIVIDUAL: US01: LINE#: {}: Death {} occurs in the future"
        return False, reason.format(self.INDI_id, self.DeathDate)

    def birth_before_marriage(self, family):
        # Story 02
        born = datetime.datetime.strptime(self.BirthDate, "%d %b %Y").date()
        for fm in family:
            if fm.HusbandID == self.INDI_id:
                marriage = datetime.datetime.strptime(fm.Married, "%d %b %Y").date()

                if born >= marriage:
                    reason = "ERROR: FAMILY: US02: LINE#: Husband's birth date {} after marriage date {}"
                    return False, reason.format(self.BirthDate, fm.Married)
            elif fm.WifeID == self.INDI_id:
                marriage = datetime.datetime.strptime(fm.Married, "%d %b %Y").date()
                if born >= marriage:
                    reason = "ERROR: FAMILY: US02: LINE#: Wife's birth date {} following marriage date {}"
                    return False, reason.format(self.BirthDate, fm.Married)
        return True

    def birth_before_death(self):
        # Story 03
        if self.DeathDate:
            death = datetime.datetime.strptime(self.DeathDate, "%d %b %Y").date()
            born = datetime.datetime.strptime(self.BirthDate, "%d %b %Y").date()
            if born < death:
                return True
            reason = "ERROR: INDIVIDUAL: US03: LINE#: {}: Died {} before born {}"
            return False, reason.format(self.INDI_id, self.DeathDate,
                                        self.BirthDate)
        return True


    def less_than_150(self):
        """
        story 7 return true if less than 150, ERROR:INDIVIAL:US07:LINE:
            More than 150 years old - Birth ... :Death ...
        """
        age = get_age(self)
        if age < 150:
            return True
        else:
            if self.DeathDate != "":
                reason = "ERROR: INDIVIDUAL: US07: LINE#: {}: More than 150 years old - Birth {} : - Death {}"
                return False, reason.format(self.INDI_id, self.BirthDate,
                                            self.DeathDate)
            else:
                reason = "ERROR: INDIVIDUAL: US07: LINE#: {}: More than 150 years old - Birth {}"
                return False, reason.format(self.INDI_id, self.BirthDate)


class Family:
    def __init__(self, ID):
        self.ID = ID
        self.Married = 'NA'
        self.Divorced = 'NA'
        self.HusbandID = 'NA'
        self.HusbandName = 'NA'
        self.WifeID = 'NA'
        self.WifeName = 'NA'
        self.Children = []

    def marry_before_current_date(self):
        # Story 01 Marry
        marry = datetime.datetime.strptime(self.Married, "%d %b %Y").date()
        if marry < date.today():
            return True
        reason = "ERROR: FAMILY: US01: LINE#: {}: Marriage date {} occurs in the future"
        return False, reason.format(self.ID, self.Married)

    def divorce_before_current_date(self):
        # Story 01 divorce
        if self.Divorced == 'NA':
            return True
        divorce = datetime.datetime.strptime(self.Divorced, "%d %b %Y").date()
        if divorce < date.today():
            return True
        reason = "ERROR: FAMILY: US01: LINE#: {}: Divorced date {} occurs in the future"
        return False, reason.format(self.ID, self.Divorced)


    def child_not_birth_before_parents_marriage(self, personObjectList):
        """
        story 8 child cannt birth before parents marriage
        return true if the child after marriage
        """
        reasonlist = []
        if self.Children:
            for cid in self.Children:
                for person in personObjectList:
                    if person.INDI_id == cid:
                        born = person.BirthDate
                        marr = self.Married
                        borndate = datetime.datetime.strptime(born, "%d %b %Y").date()
                        marrdate = datetime.datetime.strptime(marr, "%d %b %Y").date()
                        if marrdate > borndate:
                            reason = "ANOMALY: FAMILY: US08: LINE#: {}: Child {} born {} before marriage on {}"
                            reasonlist.append(reason.format(self.ID, cid,
                                                            born, marr))
        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def parents_not_marry_before_they_dead(self, personObjectList):
        # story 5
        marr = self.Married
        marrdate = datetime.datetime.strptime(marr, "%d %b %Y").date()
        reasonlist=[]
        # check Husband
        for person in personObjectList:
            if person.INDI_id == self.HusbandID:
                dead = person.DeathDate
                if(dead == ""):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if marrdate >= deathDate:

                        reason = "ANOMALY: FAMILY: US05: FAM#: {}: Married {} after husband's {} death on {}"
                        reasonlist.append(reason.format(self.ID, marr, self.HusbandID, dead ))
        # check wife
        for person in personObjectList:
            if person.INDI_id == self.WifeID:
                dead = person.DeathDate
                if(dead == ""):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if marrdate >= deathDate:
                        reason = "ANOMALY: FAMILY: US05: FAM#: {}: Married {} after wife's {} death on {}"
                        reasonlist.append(reason.format(self.ID, marr , self.WifeID, dead ))
        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def parents_not_divorce_before_they_dead(self, personObjectList):
        # story 6
        reasonlist=[]
        divc = self.Divorced
        if(divc == "NA"):
            return True
        divcdate = datetime.datetime.strptime(divc, "%d %b %Y").date()
        # check Husband
        for person in personObjectList:
            if person.INDI_id == self.HusbandID:
                dead = person.DeathDate
                if(dead == ""):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if divcdate >= deathDate:
                        reason = "ANOMALY: FAMILY: US06: FAM#: {}: Divorce {} after husband's({}) death on {}"
                        reasonlist.append(reason.format(self.ID, divc, self.HusbandID, dead ))
        # check wife
        for person in personObjectList:
            if person.INDI_id == self.WifeID:
                dead = person.DeathDate
                if(dead == ""):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if divcdate >= deathDate:
                        reason = "ANOMALY: FAMILY: US06: FAM#: {}: Divorce {} after wife's({}) death on {}"
                        reasonlist.append(reason.format(self.ID, divc, self.WifeID, dead))
        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def marriage_before_divorce(self):
        if self.Divorced != "NA":
            # print("Divorced: ", self.Divorced)
            divorce = datetime.datetime.strptime(self.Divorced,
                                                 "%d %b %Y").date()

            marry = datetime.datetime.strptime(self.Married,
                                                 "%d %b %Y").date()
            if marry < divorce:
                return True
            reason = "ERROR: INDIVIDUAL: US04: LINE#: {}: Divorced {} before married {}"
            return False, reason.format(self.ID, self.Divorced,
                                        self.Married)
        return True

    def pfamily(self):
        # print(self.ID + ' ' + self.Married + ' ' + self.Divorced + ' ' + \
        #     self.HusbandID + ' ' + self.WifeID + ' ' + \
        #     ''.join(self.Children))
        print("{0} {1} {2} {3} {4} {5}".format(
            self.ID, self.Married, self.Divorced,
            self.HusbandID, self.WifeID, self.Children))


def main():
    readFile = open(fileName, 'r')
    allContents = readFile.read().splitlines()

    allContents = [one for one in allContents if one != '']

    # eachLine = [<level>, <tag>, <arguments>]
    allLine = []
    for oneContent in allContents:
        # anayls
        oneContent = oneContent.split(' ')
        level = int(oneContent[0])
        if level == 0:
            if oneContent[1] in _TAGLIST0_1:
                tag = oneContent[1]
                argu = ' '.join(oneContent[2:])
            else:
                tag = oneContent[2]
                argu = oneContent[1]
        else:
            tag = oneContent[1]
            argu = ' '.join(oneContent[2:])
        oneContent = [level, tag, argu]
        allLine.append(oneContent)
        # print(allLine)

    # Person
    personLineList = []
    onePerson = []

    for oneline in allLine:
        if oneline[0] == 0:
            if (oneline[1] != "INDI"):
                continue
        elif oneline[0] == 1:
            if oneline[1] not in _TAGLIST1_INDI:
                continue
        else:
            if oneline[1] not in _TAGLIST2:
                continue

        if oneline[0] == 0 and oneline[1] == "INDI":
            if not onePerson:  # is empty
                onePerson.append(oneline)
            else:
                personLineList.append(onePerson)
                onePerson = []
                onePerson.append(oneline)

        else:
            onePerson.append(oneline)
    personLineList.append(onePerson)

    PersonObjectList = []
    for onePersonLine in personLineList:
        INDI_id = ""
        name = ""
        gender = ""
        BirthDate = ""
        DeathDate = ""
        FID_child = []
        FID_spouse = []
        for oneline in onePersonLine:
            if oneline[0] == 0:
                INDI_id = oneline[2]
            if oneline[0] == 1:
                if oneline[1] == "NAME":
                    name = oneline[2]
                if oneline[1] == "SEX":
                    gender = oneline[2]
                if oneline[1] == "BIRT":
                    BirthDate = "temp"
                if oneline[1] == "DEAT":
                    DeathDate = "temp"
                if oneline[1] == "FAMS":
                    FID_spouse.append(oneline[2])
                if oneline[1] == "FAMC":
                    FID_child.append(oneline[2])
            if oneline[0] == 2:
                if oneline[1] == "DATE":
                    if BirthDate == "temp":
                        BirthDate = oneline[2]
                    if DeathDate == "temp":
                        DeathDate = oneline[2]
        onePerson = Person(INDI_id, name, gender, BirthDate,
                           DeathDate, FID_child, FID_spouse)
        PersonObjectList.append(onePerson)

    # family
    family = []
    currentfamily = None
    mp = 0
    dp = 0
    for oneContent in allLine:
        if oneContent[0] == 0 and oneContent[1] == 'FAM':
            if currentfamily is not None:
                family.append(currentfamily)
                currentfamily = None
            currentfamily = Family(oneContent[2])
        if oneContent[0] == 1 and oneContent[1] == 'MARR':
            mp = 1
        if oneContent[0] == 1 and oneContent[1] == 'DIV':
            dp = 1
        if oneContent[0] == 2 and oneContent[1] == 'DATE':
            if mp == 1:
                currentfamily.Married = oneContent[2]
                mp = 0
            elif dp == 1:
                currentfamily.Divorced = oneContent[2]
                dp = 0
        if oneContent[0] == 1 and oneContent[1] == 'HUSB':
            currentfamily.HusbandID = oneContent[2]
        if oneContent[0] == 1 and oneContent[1] == 'WIFE':
            currentfamily.WifeID = oneContent[2]
        if oneContent[0] == 1 and oneContent[1] == 'CHIL':
            currentfamily.Children.append(oneContent[2])
    family.append(currentfamily)

    # Sort
    PersonObjectList.sort(key=lambda x: x.INDI_id)
    family.sort(key=lambda x: x.ID)

    # Print
    # for one in PersonObjectList:
    #     print(one.name, one.INDI_id, one.gender, one.BirthDate,
    #           one.DeathDate, one.FID_child, one.FID_spouse)

    personTable = PrettyTable()
    personTable.field_names = ["ID", "Name", "Gender", "Birthday",
                               "Age", "Alive", "Death", "Child", "Spouse"]

    for one in PersonObjectList:
        child = "NA"
        spouse = "NA"
        death = "NA"
        alive = "Y"
        born = datetime.datetime.strptime(one.BirthDate, "%d %b %Y").date()
        today = date.today()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        if one.FID_child:
            child = one.FID_child
        if one.FID_spouse:
            spouse = one.FID_spouse
        if one.DeathDate != "":
            alive = "N"
            death = one.DeathDate
            today = datetime.datetime.strptime(one.DeathDate, "%d %b %Y").date()
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

        personTable.add_row([one.INDI_id, one.name, one.gender,
                             one.BirthDate, age, alive, death, child, spouse])

    print(personTable)

    familyTable = PrettyTable()
    familyTable.field_names = ["ID", "Married", "Divorced", "Husband ID",
                               "Husband Name", "Wife ID", "Wife Name",
                               "Children"]
    for one in family:
        Children = "NA"
        if one.Children:
            Children = one.Children
        for oneP in PersonObjectList:
            if oneP.INDI_id == one.HusbandID:
                one.HusbandName = oneP.name
            if oneP.INDI_id == one.WifeID:
                one.WifeName = oneP.name

        familyTable.add_row(
            [one.ID, one.Married, one.Divorced, one.HusbandID, one.HusbandName,
             one.WifeID, one.WifeName, Children])

    print(familyTable)
    # The new add of main in project 3
    ErrorList = []
    # stories about individual
    for person in PersonObjectList:
        story01_birth = person.birth_before_current_date()
        story01_death = person.death_before_current_date()
        story02 = person.birth_before_marriage(family)
        story03 = person.birth_before_death()
        story07 = person.less_than_150()
        if story01_birth != True:
            ErrorList.append(story01_birth[1])
        if story01_death != True:
            ErrorList.append(story01_death[1])
        if story02 != True:
            ErrorList.append(story02[1])
        if story03 != True:
            ErrorList.append(story03[1])
        if story07 != True:
            ErrorList.append(story07[1])

    # stories about familiy
    for fm in family:
        story01_marry = fm.marry_before_current_date()
        story01_divorce = fm.divorce_before_current_date()
        story04 = fm.marriage_before_divorce()
        story05 = fm.parents_not_marry_before_they_dead(PersonObjectList)
        story06 = fm.parents_not_divorce_before_they_dead(PersonObjectList)
        story08 = fm.child_not_birth_before_parents_marriage(PersonObjectList)
        if story01_marry != True:
            ErrorList.append(story01_marry[1])
        if story01_divorce != True:
            ErrorList.append(story01_divorce[1])
        if story04 != True:
            ErrorList.append(story04[1])
        if story05 != True:
            for i in range(1, len(story05)):
                ErrorList.append(story05[i])
        if story06 != True:
            for i in range(1, len(story06)):
                ErrorList.append(story06[i])
        if story08 != True:
            for i in range(1, len(story08)):
                ErrorList.append(story08[i])
    for error in ErrorList:
        if isinstance(error, list):
            for e in error:
                print(e)
        else:
            print(error)


if __name__ == '__main__':
    main()
