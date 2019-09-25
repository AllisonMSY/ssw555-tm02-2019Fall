fileName = "HW2_test.txt"

_TAGLIST0_1 = ['HEAD', 'TRLR', 'NOTE']
_TAGLIST0_2 = ['INDI', 'FAM']
_TAGLIST1_INDI = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
_TAGLIST1_FAM = ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
_TAGLIST2 = ['DATE']

class Person:
    def __init__(self, name, gender, BirthDate, DeathDate, FID_child, FID_spouse)
    pass

readFile = open(fileName, 'r')
allContents = readFile.read().splitlines()

allContents = [one for one in allContents if one != '']

# eachLine = [<level>, <tag>, <arguments>]
allLine = []
for oneContent in allContents:
    print("--> " + oneContent)
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
    print(allLine)
    # output
    print("<-- ", end='')
    if oneContent[0] == 0:
        if oneContent[1] in _TAGLIST0_1 or oneContent[1] in _TAGLIST0_2:
            print(f'{oneContent[0]}|{oneContent[1]}|Y|{oneContent[2]}')
        else:
            print(f'{oneContent[0]}|{oneContent[1]}|N|{oneContent[2]}')
    elif oneContent[0] == 1:
        if oneContent[1] in _TAGLIST1_FAM or oneContent[1] in _TAGLIST1_INDI:
            print(f'{oneContent[0]}|{oneContent[1]}|Y|{oneContent[2]}')
        else:
            print(f'{oneContent[0]}|{oneContent[1]}|N|{oneContent[2]}')
    else:
        if oneContent[1] in _TAGLIST2:
            print(f'{oneContent[0]}|{oneContent[1]}|Y|{oneContent[2]}')
        else:
            print(f'{oneContent[0]}|{oneContent[1]}|N|{oneContent[2]}')