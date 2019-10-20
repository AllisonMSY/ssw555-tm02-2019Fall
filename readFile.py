_TAGLIST0_1 = ['HEAD', 'TRLR', 'NOTE']
_TAGLIST0_2 = ['INDI', 'FAM']
_TAGLIST1_INDI = ['NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS']
_TAGLIST1_FAM = ['MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV']
_TAGLIST2 = ['DATE']

def readGCFile(fileName):
    readFile = open(fileName, 'r')
    allContents = readFile.read().splitlines()
    readFile.close()

    allContents = [one for one in allContents]
    # eachLine = [<level>, <tag>, <arguments>]
    allLine = []
    lineNum = 1
    for oneContent in allContents:
        # anayls
        if oneContent == '':
            lineNum += 1
            continue
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
        oneContent = [level, tag, argu, lineNum]
        lineNum += 1
        allLine.append(oneContent)

    checkedLine = []
    for oneline in allLine:
        if oneline[0] == 0:
            if oneline[1] not in _TAGLIST0_2:
                continue
            else:
                checkedLine.append(oneline)
        elif oneline[0] == 1:
            if oneline[1] not in _TAGLIST1_FAM and oneline[1] not in _TAGLIST1_INDI:
                continue
            else:
                checkedLine.append(oneline)
        else:
            if oneline[1] not in _TAGLIST2:
                continue
            else:
                checkedLine.append(oneline)
    return checkedLine

# def main():
#     fileName = "./testFile/test_project4.txt"
#     res = readGCFile(fileName)
#     for one in res:
#         print(one)


# if __name__ == '__main__':
#     main()
