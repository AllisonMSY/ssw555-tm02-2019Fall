from prettytable import PrettyTable
from datetime import date
import datetime

fileName = "test.txt"

_TAGLIST0_1 = ['HEAD', 'TRLR', 'NOTE']
_TAGLIST0_2 = ['INDI', 'FAM']
_TAGLIST1_INDI = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
_TAGLIST1_FAM = ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
_TAGLIST2 = ['DATE']

class Person:
    def __init__(self, INDI_id, name, gender, BirthDate, DeathDate, FID_child, FID_spouse):
        self.INDI_id = INDI_id
        self.name = name
        self.gender = gender
        self.BirthDate = BirthDate
        self.DeathDate = DeathDate
        self.FID_child = FID_child
        self.FID_spouse = FID_spouse

class Family:
	def __init__(self,ID):
		self.ID = ID
		self.Married = 'NA'
		self.Divorced = 'NA'
		self.HusbandID = 'NA'
		self.HusbandName = 'NA'
		self.WifeID = 'NA'
		self.WifeName = 'NA'
		self.Children = []
	def pfamily(self):
		print(self.ID + ' ' + self.Married + ' ' +self.Divorced +' '+ self.HusbandID + ' '+ self.WifeID +' ' + ''.join(self.Children))


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
        if oneContent[1] in _TAGLIST0_1 :
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

personLineList = []
onePerson = []

for oneline in allLine:
    # ignore all useless line
    # print(oneline[1])
    # print(oneline[1] not in _TAGLIST0_2)

    if oneline[0] == 0:
        if (oneline[1] not in _TAGLIST0_2):
            continue
    elif oneline[0] == 1:
        if oneline[1] not in _TAGLIST1_INDI:
            continue
    else:
        if oneline[1] not in _TAGLIST2:
            continue

    if oneline[0] == 0 and oneline[1] == "INDI":
        if not onePerson: # is empty
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
    onePerson = Person(INDI_id,name,gender,BirthDate,DeathDate,FID_child,FID_spouse)
    PersonObjectList.append(onePerson)

family = []
currentfamily = None
mp = 0
dp = 0
for oneContent in allLine:
	if oneContent[0]==0 and oneContent[1] == 'FAM':
		if currentfamily is not None:
			family.append(currentfamily)
			currentfamily = None
		currentfamily = Family(oneContent[2])
	if oneContent[0] == 1 and oneContent[1] == 'MARR':
		mp = 1
	if oneContent[0] ==1 and oneContent[1] == 'DIV':
		dp = 1
	if oneContent[0] ==2 and oneContent[1] == 'DATE':
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
#     print(one.name, one.INDI_id, one.gender, one.BirthDate, one.DeathDate, one.FID_child, one.FID_spouse)


personTable = PrettyTable()
personTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

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
    if one.DeathDate != "" :
        alive = "N"
        death = one.DeathDate
        today = datetime.datetime.strptime(one.DeathDate, "%d %b %Y").date()
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
         

    
    personTable.add_row([one.INDI_id, one.name, one.gender, one.BirthDate, age , alive ,death , child, spouse])

print(personTable)

familyTable = PrettyTable()
familyTable.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
for one in family:
    HusbandName = ""
    WifeName = ""
    Children = "NA"
    if one.Children:
        Children = one.Children
    for oneP in PersonObjectList:
        if oneP.INDI_id == one.HusbandID:
            one.HusbandName = oneP.name
        if oneP.INDI_id == one.WifeID:
            one.WifeName = oneP.name
    
    familyTable.add_row([one.ID, one.Married, one.Divorced, one.HusbandID, one.HusbandName, one.WifeID, one.WifeName, Children])

print(familyTable)