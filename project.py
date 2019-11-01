from prettytable import PrettyTable
from datetime import date
import datetime
import collections
# custom py
import readFile
import printPrettyTable

fileName = "./testFile/test_project6.txt"

_TAGLIST0_1 = ['HEAD', 'TRLR', 'NOTE']
_TAGLIST0_2 = ['INDI', 'FAM']
_TAGLIST1_INDI = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
_TAGLIST1_FAM = ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
_TAGLIST2 = ['DATE']


def get_age(person):
    born = datetime.datetime.strptime(person.BirthDate, "%d %b %Y").date()
    if person.DeathDate != "NA":
        today = datetime.datetime.strptime(person.DeathDate, "%d %b %Y").date()
        age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))
    else:
        today = date.today()
        age = today.year - born.year - \
            ((today.month, today.day) < (born.month, born.day))
    return age
#return the year between first and second, this assume first is later than second
def get_year_gap(first,second):
    first_year = datetime.datetime.strptime(first, "%d %b %Y").date()
    second_year = datetime.datetime.strptime(second, "%d %b %Y").date()
    gap = first_year.year - second_year.year - \
          ((first_year.month, first_year.day) < (second_year.month, second_year.day))
    return gap

class Person:
    def __init__(self, INDI_id):
        self.INDI_id = INDI_id
        self.name = "NA"
        self.gender = "NA"
        self.BirthDate = "NA"
        self.DeathDate = "NA"
        self.FID_child = []
        self.FID_spouse = []
        self.ID_LINE = "NA"
        self.NAME_LINE = "NA"
        self.GENDER_LINE = "NA"
        self.BIRTH_LINE = "NA"
        self.DEATH_LINE = "NA"
        self.FAMC_LINE = []
        self.FAMS_LINE = []
    
    @staticmethod
    def list_upcoming_birthdays_from_date(personList, today):
        # story 38
        upcoming_birthdays_person_list = []
        for one in personList:
            if one.DeathDate == "NA":
                birthday = datetime.datetime.strptime(one.BirthDate, "%d %b %Y").date()
                # today = date.today()
                thisYearBirthday = birthday.replace(year=today.year)
                nextYearBirthday = birthday.replace(year=today.year+1)
                if 0 <= (thisYearBirthday - today).days <= 30 :
                    upcoming_birthdays_person_list.append(one)
                if (nextYearBirthday - today).days <= 30 :
                    upcoming_birthdays_person_list.append(one)
        print("===== UPCOMING BIRTHDAY =====")
        if upcoming_birthdays_person_list:
            printPrettyTable.printPeoplePrettyTable(upcoming_birthdays_person_list)
        else:
            print(" NULL ")
        print("=============================")
        return upcoming_birthdays_person_list

    def get_first_name(self):
        return self.name.split(' ')[0]

    def birth_before_current_date(self):
        # Story 01 Birth
        born = datetime.datetime.strptime(self.BirthDate, "%d %b %Y").date()
        if born < date.today():
            return True
        reason = "ERROR: INDIVIDUAL: US01: {}: {}: Birthday {} occurs in the future"
        return False, reason.format(self.ID_LINE, self.INDI_id, self.BirthDate)

    def death_before_current_date(self):
        # Story 01 Death
        if self.DeathDate == 'NA':
            return True
        death = datetime.datetime.strptime(self.DeathDate, "%d %b %Y").date()
        if death < date.today():
            return True
        reason = "ERROR: INDIVIDUAL: US01: {}: {}: Death {} occurs in the future"
        return False, reason.format(self.ID_LINE, self.INDI_id, self.DeathDate)

    def birth_before_marriage(self, family):
        # Story 02
        born = datetime.datetime.strptime(self.BirthDate, "%d %b %Y").date()
        for fm in family:
            if fm.HusbandID == self.INDI_id:
                marriage = datetime.datetime.strptime(fm.Married, "%d %b %Y").date()

                if born >= marriage:
                    reason = "ERROR: FAMILY: US02: {}: Husband's birth date {} after marriage date {}"
                    return False, reason.format(self.ID_LINE, self.BirthDate, fm.Married)
            elif fm.WifeID == self.INDI_id:
                marriage = datetime.datetime.strptime(fm.Married, "%d %b %Y").date()
                if born >= marriage:
                    reason = "ERROR: FAMILY: US02: {}: Wife's birth date {} following marriage date {}"
                    return False, reason.format(self.ID_LINE, self.BirthDate, fm.Married)
        return True

    def birth_before_death(self):
        # Story 03
        if self.DeathDate != "NA":
            death = datetime.datetime.strptime(self.DeathDate, "%d %b %Y").date()
            born = datetime.datetime.strptime(self.BirthDate, "%d %b %Y").date()
            if born < death:
                return True
            reason = "ERROR: INDIVIDUAL: US03: {}: {}: Died {} before born {}"
            return False, reason.format(self.ID_LINE, self.INDI_id, self.DeathDate,
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
            if self.DeathDate != "NA":
                reason = "ERROR: INDIVIDUAL: US07:{}: {}: More than 150 years old - Birth {} : - Death {}"
                return False, reason.format(self.BIRTH_LINE,self.INDI_id, self.BirthDate,
                                            self.DeathDate)
            else:
                reason = "ERROR: INDIVIDUAL: US07:{}: {}: More than 150 years old - Birth {}"
                return False, reason.format(self.BIRTH_LINE,self.INDI_id, self.BirthDate)

    def unique_person_id(self, personObjectList):
        #story 22-1
        reasonList=[]
        person_dict = dict()
        for person in personObjectList:
            if person.INDI_id in person_dict:
                reason = "ERROR: INDIVIDUAL: US22: {}: {} is not a unique ID"
                reasonList.append(reason.format(person.ID_LINE, person.INDI_id))
            else:
                person_dict[person.INDI_id] = 1
        if not reasonList:
            return True
        else:
            return False, reasonList

    def unique_name_and_birth_date(self, personObjectList):
        # story 23
        name_birth_dict = collections.defaultdict(int)
        reason_list = []
        reason = "ERROR: INDIVIDUAL: US23:{}: Name {}: {} Birth {} are not unique"
        for person in personObjectList:
            name_birth_dict[(person.name, person.BirthDate)] += 1
            if name_birth_dict[(person.name, person.BirthDate)] > 1:
                reason_list.append(reason.format(
                    person.ID_LINE, person.name, person.BIRTH_LINE, person.BirthDate))
        if reason_list:
            return False, reason_list
        return True

    def pPerson(self):
        print("{0} {1} {2} {3} {4} {5} {6}".format(
            self.INDI_id, self.name, self.gender,
            self.BirthDate, self.DeathDate, self.FID_child, self.FID_spouse) )
        print("{0} {1} {2} {3} {4} {5} {6}".format(
            self.ID_LINE, self.NAME_LINE, self.GENDER_LINE, self.BIRTH_LINE,
            self.DEATH_LINE, self.FAMC_LINE, self.FAMS_LINE) )

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
        self.ID_LINE = "NA"
        self.MARRAY_LINE = "NA"
        self.DIVORCED_LINE = "NA"
        self.HUSBAND_LINE = "NA"
        self.WIFE_LINE = "NA"
        self.CHILDREN_LINE = []

    @staticmethod
    def list_upcoming_anniversaries_from_date(familyList, personList, today):
        # story 39
        upcoming_anniversaries_family_list = []
        for oneFamily in familyList:
            if oneFamily.Divorced == "NA": # not divorced
                for onePerson in personList:
                    if onePerson.INDI_id == oneFamily.HusbandID or onePerson.INDI_id == oneFamily.WifeID:
                        if onePerson.DeathDate != 'NA':
                            break
                else: # couple not dead
                    anniversary = datetime.datetime.strptime(oneFamily.Married, "%d %b %Y").date()
                    # today = date.today()
                    thisYearAnniversary = anniversary.replace(year=today.year)
                    nextYearAnniversary = anniversary.replace(year=today.year+1)
                    if 0 <= (thisYearAnniversary - today).days <= 30 :
                        upcoming_anniversaries_family_list.append(oneFamily)
                    if (nextYearAnniversary - today).days <= 30:
                        upcoming_anniversaries_family_list.append(oneFamily)
                
        print("===== UPCOMING ANNIVERSARY =====")
        if upcoming_anniversaries_family_list:
            printPrettyTable.printFamilyPrettyTable(upcoming_anniversaries_family_list,personList)
        else:
            print("NULL")
        print("================================")
        return upcoming_anniversaries_family_list

    def marry_before_current_date(self):
        # Story 01 Marry
        marry = datetime.datetime.strptime(self.Married, "%d %b %Y").date()
        if marry < date.today():
            return True
        reason = "ERROR: FAMILY: US01: {}: {}: Marriage date {} occurs in the future"
        return False, reason.format(self.ID_LINE, self.ID, self.Married)

    def divorce_before_current_date(self):
        # Story 01 divorce
        if self.Divorced == 'NA':
            return True
        divorce = datetime.datetime.strptime(self.Divorced, "%d %b %Y").date()
        if divorce < date.today():
            return True
        reason = "ERROR: FAMILY: US01: {}: {}: Divorced date {} occurs in the future"
        return False, reason.format(self.ID_LINE, self.ID, self.Divorced)

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
                        marryDate = datetime.datetime.strptime(marr, "%d %b %Y").date()
                        if marryDate > borndate:
                            reason = "ANOMALY: FAMILY: US08:{}: {}: Child {} born {} before marriage on {}"
                            reasonlist.append(reason.format(self.MARRAY_LINE, self.ID, cid,
                                                            born, marr))
        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def parents_not_marry_before_they_dead(self, personObjectList):
        # story 05
        marr = self.Married
        marryDate = datetime.datetime.strptime(marr, "%d %b %Y").date()
        reasonlist=[]
        # check Husband
        for person in personObjectList:
            if person.INDI_id == self.HusbandID:
                dead = person.DeathDate
                if(dead == "NA"):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if marryDate >= deathDate:

                        reason = "ANOMALY: FAMILY: US05: {}: Married {} after husband's({}) death on {}"
                        reasonlist.append(reason.format(self.MARRAY_LINE, marr, self.HusbandID, dead ))
        # check wife
        for person in personObjectList:
            if person.INDI_id == self.WifeID:
                dead = person.DeathDate
                if(dead == "NA"):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if marryDate >= deathDate:
                        reason = "ANOMALY: FAMILY: US05: {}: Married {} after wife's({}) death on {}"
                        reasonlist.append(reason.format(self.MARRAY_LINE, marr , self.WifeID, dead ))
        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def parents_not_divorce_before_they_dead(self, personObjectList):
        # story 06
        reasonlist=[]
        divc = self.Divorced
        if(divc == "NA"):
            return True
        divcdate = datetime.datetime.strptime(divc, "%d %b %Y").date()
        # check Husband
        for person in personObjectList:
            if person.INDI_id == self.HusbandID:
                dead = person.DeathDate
                if(dead == "NA"):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if divcdate >= deathDate:
                        reason = "ANOMALY: FAMILY: US06: {}: Divorce {} after husband's({}) death on {}"
                        reasonlist.append(reason.format(self.DIVORCED_LINE, divc, self.HusbandID, dead ))
        # check wife
        for person in personObjectList:
            if person.INDI_id == self.WifeID:
                dead = person.DeathDate
                if(dead == "NA"):
                    break
                else:
                    deathDate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                    if divcdate >= deathDate:
                        reason = "ANOMALY: FAMILY: US06: {}: Divorce {} after wife's({}) death on {}"
                        reasonlist.append(reason.format(self.DIVORCED_LINE, divc, self.WifeID, dead))
        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def marriage_before_divorce(self):
        # story 04
        if self.Divorced != "NA":
            # print("Divorced: ", self.Divorced)
            divorce = datetime.datetime.strptime(self.Divorced,
                                                 "%d %b %Y").date()

            marry = datetime.datetime.strptime(self.Married,
                                                 "%d %b %Y").date()
            if marry < divorce:
                return True
            reason = "ERROR: INDIVIDUAL: US04: {}: {}: Divorced {} before married {}"
            return False, reason.format(self.ID_LINE, self.ID, self.Divorced,
                                        self.Married)
        return True

    def marriage_after_14(self,personObjectList):
        #story 10
        reasonList = []
        if self.Married != "NA":
            for person in personObjectList:
                if person.INDI_id == self.HusbandID:
                    if get_year_gap(self.Married,person.BirthDate)<14:
                        reason = "ERROR:FAMILY:US10:{}: {}: Marriage {} before husband ({}) who born on {} was 14 years old"
                        reasonList.append(reason.format(self.MARRAY_LINE,self.ID,self.Married,self.HusbandID,person.BirthDate))
                elif person.INDI_id == self.WifeID:
                    if get_year_gap(self.Married,person.BirthDate)<14:
                        reason = "ERROR:FAMILY:US10:{}: {}: Marriage {} before wife ({}) who born on {} was 14 years old"
                        reasonList.append(reason.format(self.MARRAY_LINE,self.ID,self.Married,self.WifeID,person.BirthDate))
        if not reasonList:
            return True
        else:
            return False,reasonList

    def unique_families_by_spouses(self, family):
        # story 24
        spouse_marry_dict = collections.defaultdict(int)
        reason_list = []
        reason = "ERROR: INDIVIDUAL: US24:{}: Husband {} Wife {}: Married {} are not unique"
        for f in family:
            spouse_marry_dict[(f.HusbandName, f.WifeName, f.Married)] += 1
            if spouse_marry_dict[(f.HusbandName, f.WifeName, f.Married)] > 1:
                reason_list.append(reason.format(
                    f.ID_LINE, f.HusbandName, f.WifeName, f.Married))
        if reason_list:
            return False, reason_list
        return True

    def unique_first_name_in_family(self,personObjectList):
        #story 25
        reasonList=[]
        firstname = dict()
        reason = "ERROR:Family:US25:{}:{}:In famliy {}, {} and {} have same first name {}"
        for person in personObjectList:
            if person.INDI_id == self.HusbandID:
                if person.get_first_name() in firstname:
                    reasonList.append(reason.format(person.NAME_LINE,self.HusbandID,self.ID,firstname[person.get_first_name()],self.HusbandID,person.get_first_name()))
                else:
                    firstname[person.get_first_name()]=person.INDI_id
            if person.INDI_id == self.WifeID:
                if person.get_first_name() in firstname:
                    reasonList.append(reason.format(person.NAME_LINE,self.WifeID,self.ID,firstname[person.get_first_name()],self.WifeID,person.get_first_name()))
                else:
                    firstname[person.get_first_name()]=person.INDI_id
            for child in self.Children:
                if person.INDI_id == child:
                    if person.get_first_name() in firstname:
                        reasonList.append(reason.format(person.NAME_LINE, child, self.ID, firstname[person.get_first_name()],child, person.get_first_name()))
                    else:
                        firstname[person.get_first_name()]=person.INDI_id
        if not reasonList:
            return True
        else:
            return False,reasonList

    def birth_before_death_of_parents(self, personObjectList):
        # story 09
        reasonlist = []
        if self.Children:
            for idx, cid in enumerate(self.Children):
                for person in personObjectList:
                    if person.INDI_id == cid:
                        born = person.BirthDate
                        borndate = datetime.datetime.strptime(born, "%d %b %Y").date()
                        # check Husband
                        for person in personObjectList:
                            if person.INDI_id == self.HusbandID:
                                dead = person.DeathDate
                                if (dead == "NA"):
                                    break
                                else:
                                    borndate_y = datetime.datetime.strptime(born, "%d %b %Y").year
                                    deathdate_y = datetime.datetime.strptime(dead, "%d %b %Y").year
                                    borndate_m = datetime.datetime.strptime(born, "%d %b %Y").month
                                    deathdate_m = datetime.datetime.strptime(dead, "%d %b %Y").month

                                    if (borndate_y - deathdate_y) * 12 + (borndate_m - deathdate_m) > 9:
                                        reason = "ANOMALY: FAMILY: US09: {}: {}: Child {} born {} after 9 month after husband's({}) death on {}"
                                        if self.CHILDREN_LINE:
                                            reasonlist.append(reason.format(self.CHILDREN_LINE[idx], self.ID, cid, born, self.HusbandID, dead))
                                        else:
                                            reasonlist.append(reason.format(None, self.ID, cid, born, self.HusbandID, dead))
                        # check wife
                        for person in personObjectList:
                            if person.INDI_id == self.WifeID:
                                dead = person.DeathDate
                                if (dead == "NA"):
                                    break
                                else:
                                    deathdate = datetime.datetime.strptime(dead, "%d %b %Y").date()
                                    if borndate > deathdate:
                                        reason = "ANOMALY: FAMILY: US09: {}: {}: Child {} born {} after wife's({}) death on {}"
                                        if self.CHILDREN_LINE:
                                            reasonlist.append(reason.format(self.CHILDREN_LINE[idx], self.ID, cid, born, self.WifeID, dead))
                                        else:
                                            reasonlist.append(reason.format(None, self.ID, cid, born, self.WifeID, dead))

        if not reasonlist:
            return True
        else:
            return False, reasonlist

    def unique_family_id(self, family):
        #story 22-2
        reasonList=[]
        family_dict = dict()
        for fm in family:
            if fm.ID in family_dict:
                reason = "ERROR: FAMILY: US22: {}: {} is not a unique ID"
                reasonList.append(reason.format(fm.ID_LINE, fm.ID))
            else:
                family_dict[fm.ID] = 1
        if not reasonList:
            return True
        else:
            return False, reasonList

    def pfamily(self):
        print("{0} {1} {2} {3} {4} {5}".format(
            self.ID, self.Married, self.Divorced,
            self.HusbandID, self.WifeID, self.Children))
        print("{0} {1} {2} {3} {4} {5}".format(
            self.ID_LINE, self.MARRAY_LINE, self.DIVORCED_LINE,
            self.HUSBAND_LINE, self.WIFE_LINE, self.CHILDREN_LINE))


def main():
    allLine = readFile.readGCFile(fileName)
    # Person
    personLineList = []
    onePerson = []

    # perpare for looping people
    for oneline in allLine:
        # if oneline[0] == 0:
        #     if (oneline[1] != "INDI"):
        #         continue
        # elif oneline[0] == 1:
        #     if oneline[1] not in _TAGLIST1_INDI:
        #         continue
        # else:
        #     if oneline[1] not in _TAGLIST2:
        #         continue

        if oneline[0] == 0:
            if oneline[1] == "INDI":
                if not onePerson:  # not have a person
                    onePerson.append(oneline)
                else: # have a person
                    personLineList.append(onePerson)
                    onePerson = []
                    onePerson.append(oneline)
            else: # hit FIM
                if onePerson: # have a person
                    personLineList.append(onePerson)
                    onePerson = []

        else:
            if onePerson:
                onePerson.append(oneline)

    if onePerson: ## append last person
        personLineList.append(onePerson)

    # create object
    PersonObjectList = []
    for onePersonAllLine in personLineList:
        INDI_id, name, gender, BirthDate, DeathDate = "NA", "NA", "NA", "NA", "NA"
        FID_child = []
        FID_spouse = []
        ID_LINE, NAME_LINE, GENDER_LINE, BIRTH_LINE, DEATH_LINE = "NA", "NA", "NA", "NA", "NA"
        FAMC_LINE, FAMS_LINE = [], []
        for oneline in onePersonAllLine:
            if oneline[0] == 0:
                INDI_id = oneline[2]
                ID_LINE = oneline[3]
            if oneline[0] == 1:
                if oneline[1] == "NAME":
                    name = oneline[2]
                    NAME_LINE = oneline[3]
                if oneline[1] == "SEX":
                    gender = oneline[2]
                    GENDER_LINE = oneline[3]
                if oneline[1] == "BIRT":
                    BirthDate = "temp"
                if oneline[1] == "DEAT":
                    DeathDate = "temp"
                if oneline[1] == "FAMS":
                    FID_spouse.append(oneline[2])
                    FAMS_LINE.append(oneline[3])
                if oneline[1] == "FAMC":
                    FID_child.append(oneline[2])
                    FAMC_LINE.append(oneline[3])
            if oneline[0] == 2:
                if oneline[1] == "DATE":
                    if BirthDate == "temp":
                        BirthDate = oneline[2]
                        BIRTH_LINE = oneline[3]
                    if DeathDate == "temp":
                        DeathDate = oneline[2]
                        DEATH_LINE = oneline[3]
        onePerson = Person(INDI_id)
        onePerson.name, onePerson.gender, onePerson.BirthDate, onePerson.DeathDate = name, gender, BirthDate, DeathDate
        onePerson.FID_child, onePerson.FID_spouse = FID_child, FID_spouse
        onePerson.ID_LINE, onePerson.NAME_LINE, onePerson.GENDER_LINE, onePerson.BIRTH_LINE, onePerson.DEATH_LINE = ID_LINE, NAME_LINE, GENDER_LINE, BIRTH_LINE, DEATH_LINE
        onePerson.FAMC_LINE, onePerson.FAMS_LINE = FAMC_LINE, FAMS_LINE
        PersonObjectList.append(onePerson)

    # # Test the line number
    # for one in PersonObjectList:
    #     one.pPerson()


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
            currentfamily.ID_LINE = oneContent[3]
        if oneContent[0] == 1 and oneContent[1] == 'MARR':
            mp = 1
        if oneContent[0] == 1 and oneContent[1] == 'DIV':
            dp = 1
        if oneContent[0] == 2 and oneContent[1] == 'DATE':
            if mp == 1:
                currentfamily.Married = oneContent[2]
                currentfamily.MARRAY_LINE = oneContent[3]
                mp = 0
            elif dp == 1:
                currentfamily.Divorced = oneContent[2]
                currentfamily.DIVORCED_LINE = oneContent[3]
                dp = 0
        if oneContent[0] == 1 and oneContent[1] == 'HUSB':
            currentfamily.HusbandID = oneContent[2]
            currentfamily.HUSBAND_LINE = oneContent[3]
        if oneContent[0] == 1 and oneContent[1] == 'WIFE':
            currentfamily.WifeID = oneContent[2]
            currentfamily.WIFE_LINE = oneContent[3]
        if oneContent[0] == 1 and oneContent[1] == 'CHIL':
            currentfamily.Children.append(oneContent[2])
            currentfamily.CHILDREN_LINE.append(oneContent[3])
    family.append(currentfamily)

    # # Test the line number
    # for one in family:
    #     one.pfamily()

    # Sort all people and family by id
    PersonObjectList.sort(key=lambda x: x.INDI_id)
    family.sort(key=lambda x: x.ID)

    # Print
    # print person
    printPrettyTable.printPeoplePrettyTable(PersonObjectList)
    
    # print family
    printPrettyTable.printFamilyPrettyTable(family,PersonObjectList)

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

    story22 = person.unique_person_id(PersonObjectList)
    if story22 != True:
        ErrorList.append(story22[1])

    story23 = person.unique_name_and_birth_date(PersonObjectList)
    if story23 != True:
        ErrorList.append(story23[1])

    # stories about family
    for fm in family:
        story01_marry = fm.marry_before_current_date()
        story01_divorce = fm.divorce_before_current_date()
        story04 = fm.marriage_before_divorce()
        story05 = fm.parents_not_marry_before_they_dead(PersonObjectList)
        story06 = fm.parents_not_divorce_before_they_dead(PersonObjectList)
        story08 = fm.child_not_birth_before_parents_marriage(PersonObjectList)
        story09 = fm.birth_before_death_of_parents(PersonObjectList)
        story10 = fm.marriage_after_14(PersonObjectList)
        story25 = fm.unique_first_name_in_family(PersonObjectList)

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
        if story09 != True:
            for i in range(1, len(story09)):
                ErrorList.append(story09[i])

        if story10 != True:
            for i in range(1,len(story10)):
                ErrorList.append(story10[i])
        if story25 != True:
            for i in range(1,len(story25)):
                ErrorList.append(story25[i])

    story22 = fm.unique_family_id(family)
    if story22 != True:
        for i in range(1, len(story22)):
            ErrorList.append(story22[i])

    story24 = fm.unique_families_by_spouses(family)
    if story24 != True:
        for i in range(1, len(story24)):
            ErrorList.append(story24[i])

    for error in ErrorList:
        if isinstance(error, list):
            for e in error:
                print(e)
        else:
            print(error)

    # Print upcoming list
    Person.list_upcoming_birthdays_from_date(PersonObjectList, date.today())
    Family.list_upcoming_anniversaries_from_date(family, PersonObjectList, date.today())

if __name__ == '__main__':
    main()
