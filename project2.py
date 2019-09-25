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

print(allLine)
print(allLine[2][1])
print(allLine[2][1] not in _TAGLIST0_2)
print("-----------")
for oneline in allLine:
    # ignore all useless line
    print(oneline[1])
    print(oneContent[1] not in _TAGLIST0_2)

    if oneline[0] == 0:
        # print(oneContent[1] in _TAGLIST0_2)
        if (oneContent[1] not in _TAGLIST0_2):
            continue
    elif oneline[0] == 1:
        if oneline[1] not in _TAGLIST1_FAM or oneline[1] not in _TAGLIST1_INDI:
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


# for i in personLineList:
#     print(i)
#     print() 

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

for one in PersonObjectList:
    print(one.name, one.INDI_id, one.gender, one.BirthDate, one.DeathDate, one.FID_child, one.FID_spouse)
    # # output
    # print("<-- ", end='')
    # if oneContent[0] == 0:
    #     if oneContent[1] in _TAGLIST0_1 or oneContent[1] in _TAGLIST0_2:
    #         print(f'{oneContent[0]}|{oneContent[1]}|Y|{oneContent[2]}')
    #     else:
    #         print(f'{oneContent[0]}|{oneContent[1]}|N|{oneContent[2]}')
    # elif oneContent[0] == 1:
    #     if oneContent[1] in _TAGLIST1_FAM or oneContent[1] in _TAGLIST1_INDI:
    #         print(f'{oneContent[0]}|{oneContent[1]}|Y|{oneContent[2]}')
    #     else:
    #         print(f'{oneContent[0]}|{oneContent[1]}|N|{oneContent[2]}')
    # else:
    #     if oneContent[1] in _TAGLIST2:
    #         print(f'{oneContent[0]}|{oneContent[1]}|Y|{oneContent[2]}')
    #     else:
    #         print(f'{oneContent[0]}|{oneContent[1]}|N|{oneContent[2]}')

