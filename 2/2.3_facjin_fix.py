import csv
import re
import numpy as np
from collections import Counter

# name = input()
name = "vacancies_big.csv"
# name = "custom_test.csv"
A = []
B = []
C = []


def shortSortReversed(val):
    return -int(str((float(val[sToIdx]) + float(val[sFromIdx])) / 2).partition('.')[0])


def contSortKey(val):
    return val[areaIdx]


def contMiddleKey(val):
    return val[2] / val[1]

def saoSort(val):
    return int(str((float(val[sToIdx]) + float(val[sFromIdx])) / 2).partition('.')[0])


total = 0
skip = 0
with open(name, encoding='utf-8-sig') as f:
    tab = csv.reader(f)
    first = None
    for row in tab:
        total = total + 1
        cont = False
        if first is None:
            first = row
            continue
        for i in row:
            if len(i) == 0:
                cont = True
        if cont:
            skip = skip + 1
            continue
        if row[first.index("salary_currency")] != "RUR":
            skip = skip + 1
            continue
        if len(row) == len(first):
            A.append(row)

# region indexes
nameIdx = first.index("name")  # 0
skillsIdx = first.index("key_skills")  # 1
premiumIdx = first.index("premium")  # 2
empNameIdx = first.index("employer_name")  # 3
sFromIdx = first.index("salary_from")  # 4
sToIdx = first.index("salary_to")  # 5
currIdx = first.index("salary_currency")  # 6
areaIdx = first.index("area_name")  # 7
# endregion


# if name == "vacancies_small.csv":
#     print(str(skip) +" из "+ str(total))
for x in A:
    for i in x:
        i = re.sub(r'<[^<>]*>', '', i)
        i = re.sub(r'\n', ', ', i)
        i = str.strip(re.sub(r'\s+', ' ', i))
        B.append(i)
if len(B) > 0:
    split = np.array_split(B, len(B) / len(first))
    skills = []
    for arr in split:
        for q in arr[1].split(','):

            skillstemp = q.lstrip().rstrip()
            skills.append(skillstemp)
        C.append(arr)

    salary_max = []
    sortedC = C
    sortedC.sort(key=shortSortReversed)




    # tempList = sortedC[-10:]
    # tempList.sort(key=shortSortReversed)
    num = 0
    print("Самые высокие зарплаты:")
    for s in sortedC[:10]:
        num = num + 1
        print("    " + str(num) + ") " + s[nameIdx] + " в компании \"" + s[empNameIdx] + "\" - " + str((float(s[sFromIdx]) + float(s[sToIdx])) / 2).partition('.')[0] + " рублей (г. " + s[areaIdx] + ")")

    print()

    # tempListSnd = sortedC[:10]
    # tempList.sort(key=shortSortReversed)

    sortedC.sort(key=saoSort)
    num = 0
    print("Самые низкие зарплаты:")
    for s in sortedC[:10]:
        num = num + 1
        print("    " + str(num) + ") " + s[nameIdx] + " в компании \"" + s[empNameIdx] + "\" - " + str((float(s[sFromIdx]) + float(s[sToIdx])) / 2).partition('.')[0] + " рублей (г. " + s[areaIdx] + ")")


        # старый алг
        # if len(salary_max) < 10:
        #     salary_max.append(sub)
        #     continue
        # if float(salary_max[len(salary_max) - 1][sToIdx]) < float(sub[sToIdx]):
        #     salary_max.append(sub)
        #     salary_max.sort(key=sort_key_max)
        # if len(salary_max) > 10:
        #     salary_max.pop(0)

    # salary_min = []
    # for sub in sortedC:
    #     if len(salary_min) < 10:
    #         salary_min.append(sub)
    #         continue
    #     if float(salary_min[len(salary_min) - 1][sFromIdx]) > float(sub[sFromIdx]):
    #         salary_min.append(sub)
    #         salary_min.sort(key=sort_key_min)
    #     if len(salary_min) > 10:
    #         salary_min.pop()

    # salary_min.reverse()
    # print("Самые высокие зарплаты:")
    # num = 0
    # for s in reversed(salary_max):
    #     num = num + 1
    #     print("    " + str(num) + ") " + s[nameIdx] + " в компании \"" + s[empNameIdx] + "\" - " +
    #           str((float(s[sFromIdx]) + float(s[sToIdx])) / 2).partition('.')[0] + " рублей (г. " + s[areaIdx] + ")")

    # num = 0
    # print()
    # print("Самые низкие зарплаты:")
    # for s in reversed(salary_min):
    #     num = num + 1
    #     print("    " + str(num) + ") " + s[nameIdx] + " в компании \"" + s[empNameIdx] + "\" - " +
    #           str((float(s[sFromIdx]) + float(s[sToIdx])) / 2).partition('.')[0] + " рублей (г. " + s[areaIdx] + ")")

    contr = Counter(skills)
    skillsCount = 10
    if len(contr) < 10:
        skillsCount = len(contr.most_common())

    skilsyTempCount = len(set(skills))
    print()

    # if name == "vacancies_small.csv":
    #     skilsyTempCount = 306

    print("Из " + str(skilsyTempCount) + " скиллов, самыми популярными являются:")
    for i in range(1, skillsCount + 1):
        adder = " раз"
        if str(contr.most_common(skillsCount)[i - 1][1])[
            len(str(contr.most_common(skillsCount)[i - 1][1])) - 1] == "2" or \
                str(contr.most_common(skillsCount)[i - 1][1])[
                    len(str(contr.most_common(skillsCount)[i - 1][1])) - 1] == "3" or \
                str(contr.most_common(skillsCount)[i - 1][1])[
                    len(str(contr.most_common(skillsCount)[i - 1][1])) - 1] == "4":
            adder = " раза"
        print("    " + str(i) + ") " + contr.most_common(skillsCount)[i - 1][0] + " - упоминается " + str(
            contr.most_common(skillsCount)[i - 1][1]) + adder)

    print()

    C.sort(key=contSortKey)
    firstCont = None
    conListCount = 0
    finalPrice = 0
    D = []
    for cont in C:
        if firstCont is None:
            firstCont = cont[areaIdx]

        if firstCont == cont[areaIdx]:
            conListCount = conListCount + 1
            finalPrice = finalPrice + int(str((float(cont[sToIdx]) + float(cont[sFromIdx])) / 2).partition('.')[0])
        else:
            D.append([firstCont, conListCount, finalPrice])
            firstCont = cont[areaIdx]
            conListCount = 1
            finalPrice = int(str((float(cont[sToIdx]) + float(cont[sFromIdx])) / 2).partition('.')[0])
    D.append([firstCont, conListCount, finalPrice])
    D.sort(key=contMiddleKey)
    D.reverse()
    num = 0
    contCount = 10;
    if len(D) < 10:
        contCount = len(D)

    print("Из " + str(len(D)) + " городов, самые высокие средние ЗП:")

    for s in D:
        if s[1] < len(C) / 100: continue
        num = num + 1
        if num > contCount:
            break
        adder = " вакансия"
        if str(s[1])[
            len(str(s[1])) - 1] == "2" or \
                str(s[1])[
                    len(str(s[1])) - 1] == "3" or \
                str(s[1])[
                    len(str(s[1])) - 1] == "4":
            adder = " вакинсии"
        elif str(s[1])[
            len(str(s[1])) - 1] != "1":
            adder = " вакинсий"

        print("    " + str(num) + ") " + s[0] + " - " + "средняя зарплата " + str(
            int(str(s[2] / s[1]).partition('.')[0])) + ' рублей' + " (" + str(s[1]) + adder + ")")
