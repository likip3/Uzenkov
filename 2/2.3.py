import csv
import re
import numpy as np
from collections import Counter

# name = input()
name = "vacancies_big.csv"
A = []
B = []
C = []


def sort_key(vac):
    return int(vac[7].partition('.')[0])


def contSortKey(val):
    return val[10]

def contMiddleKey(val):
    return val[2]/val[1]


with open(name, encoding='utf-8-sig') as f:
    tab = csv.reader(f)
    first = None
    for row in tab:
        cont = False
        if first is None:
            first = row
            continue
        for i in row:
            if len(i) == 0:
                cont = True
        if cont:
            continue
        if row[9] != "RUR":
            continue
        if len(row) == len(first):
            A.append(row)

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
        for q in arr[2].split(','):
            skills.append(q.lstrip())
        C.append(arr)

    salary_max = []
    for sub in C:
        if len(salary_max) < 10:
            salary_max.append(sub)
            continue
        if float(salary_max[len(salary_max) - 1][7]) < float(sub[7]):
            salary_max.append(sub)
            salary_max.sort(key=sort_key)
        if len(salary_max) > 10:
            salary_max.pop(0)

    salary_min = []
    for sub in C:
        if len(salary_min) < 10:
            salary_min.append(sub)
            continue
        if float(salary_min[len(salary_min) - 1][7]) > float(sub[7]):
            salary_min.append(sub)
            salary_min.sort(key=sort_key)
        if len(salary_min) > 10:
            salary_min.pop()

    salary_max.reverse()
    print("Самые высокие зарплаты:")
    num = 0
    for s in salary_max:
        num = num + 1
        print(str(num) + ") " + s[0] + "в компании \""+ s[4] + "\" - " + s[7].partition('.')[0] + " рублей (г. " + s[10] + ")")

    num = 0
    print()
    print("Самые низкие зарплаты:")
    for s in salary_min:
        num = num + 1
        print(str(num) + ") " + s[0] + "в компании \""+ s[4] + "\" - " + s[7].partition('.')[0] + " рублей (г. " + s[10] + ")")

    contr = Counter(skills)
    skillsCount = 10
    print()
    print("Из " + str(skillsCount) + " скиллов, самыми популярными являются:")
    for i in range(1, skillsCount + 1):
        adder = " раз"
        if str(contr.most_common(skillsCount)[i - 1][1])[
            len(str(contr.most_common(skillsCount)[i - 1][1])) - 1] == "2" or \
                str(contr.most_common(skillsCount)[i - 1][1])[
                    len(str(contr.most_common(skillsCount)[i - 1][1])) - 1] == "3" or \
                str(contr.most_common(skillsCount)[i - 1][1])[
                    len(str(contr.most_common(skillsCount)[i - 1][1])) - 1] == "4":
            adder = " раза"
        print(str(i) + ") " + contr.most_common(skillsCount)[i - 1][0] + " - упоминается " + str(
            contr.most_common(skillsCount)[i - 1][1]) + adder)

    print()
    contCount=10;
    print("Из "+str(contCount)+" городов, самые высокие средние ЗП:")

    C.sort(key=contSortKey)
    firstCont = None
    conListCount = 0
    finalPrice = 0
    D = []
    for cont in C:
        if firstCont is None:
            firstCont = cont[10]

        if firstCont == cont[10]:
            conListCount = conListCount+1
            finalPrice = finalPrice + int(cont[7].partition('.')[0])
        else:
            D.append([firstCont,conListCount,finalPrice])
            firstCont = cont[10]
            conListCount = 1
            finalPrice = int(cont[7].partition('.')[0])

    D.sort(key=contMiddleKey)
    D.reverse()
    num = 0
    for s in D:
        if s[1]<len(C)/100: continue
        num = num + 1
        if num>contCount:
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

        print(str(num) + ") " + s[0] + " - " +"средняя зарплата " + str(int(str(s[2]/s[1]).partition('.')[0])) + ' рублей' +" ("+ str(s[1])+" "+adder+")")
