import csv
import math
import re
import sys

# import datetime
from prettytable import PrettyTable

name = input()
# name = 'vacancies_medium.csv'
# name = 'empty.csv'

# region val
A = []
B = []
C = []
temp = 0
first = None


# endregion

# region Funk
def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


def split_equal(lst):
    len_ = len(lst)

    subLen = 12
    return [lst[i:i + subLen] for i in range(0, len_, subLen)]


def ApproveFile():
    if first is None:
        print("Пустой файл")
        sys.exit()
    if len(A) == 0:
        print("Нет данных")
        sys.exit()


def ConvertTax():
    if C[k][index] == "Нет":
        C[k][index] = "С вычетом налогов"
    if C[k][index] == "Да":
        C[k][index] = "Без вычета налогов"


def NewAppendFormat():
    formatRowTableList.append(
        '{0:,}'.format(int(C[k][6].partition('.')[0])).replace(',', ' ') + ' - ' + '{0:,}'.format(
            int(C[k][7].partition('.')[0])).replace(',', ' ') + ' (' + C[k][index] + ')' + ' (' + C[k][
            index - 1] + ')')


def ReformatFile():
    global i
    for x in A:
        for i in x:
            i = re.sub(r'<[^<>]*>', '', i)
            i = re.sub(r'\n', ', ', i)
            i = str.strip(re.sub(r'\s+', ' ', i))
            B.append(i)


def AllowRows():
    global first, i
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
        if len(row) == len(first):
            A.append(row)


# endregion


with open(name, encoding='utf-8-sig') as f:
    tab = csv.reader(f)
    AllowRows()
    ApproveFile()

ReformatFile()
# region Dict
replacements = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
                'premium': 'Премиум-вакансия', 'employer_name': 'Компания',
                'salary_from': 'Нижняя граница вилки оклада', 'salary_to': 'Верхняя граница вилки оклада',
                'salary_gross': 'Оклад указан до вычета налогов', 'salary_currency': 'Идентификатор валюты оклада',
                'area_name': 'Название региона', 'published_at': 'Дата публикации вакансии'
                }

repDict = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет", "between3And6": "От 3 до 6 лет",
           "moreThan6": "Более 6 лет", "AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро",
           "GEL": "Грузинский лари", "KGS": "Киргизский сом",
           "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум", "True": "Да",
           "False": "Нет"
           }
# endregion

table = PrettyTable(hrules=1, align="l")
table.field_names = ["№", "Название", "Описание", "Навыки", "Опыт работы", "Премиум-вакансия", "Компания", "Оклад",
                     "Название региона", "Дата публикации вакансии"]
table.max_width = 20
formatRowTableList = []
replacer = replacements.get
first = [replacer(n, n) for n in first]
if len(B) > 0:
    split = split_equal(B)

    for arr in split:
        C.append(arr)

    for k in range(0, len(C)):
        formatRowTableList.append(str(k + 1))
        for index in range(0, len(first)):
            # if index == 4 or index == 8 or index == 9 or index == 3:
            if index == 6 or index == 7:
                temp = temp + int(C[k][index].partition('.')[0])
                continue

            for word, initial in repDict.items():
                if C[k][index] == word:
                    C[k][index] = initial
            if index == 8:
                ConvertTax()
                continue
            if index == 11:
                C[k][index] = C[k][index][8:10] + '.' + C[k][index][5:7] + '.' + C[k][index][0:4]
            if index == 9:
                NewAppendFormat()
                temp = 0
                continue
            if index == 2:
                C[k][index] = C[k][index].replace(", ", "\n")
            if len(C[k][index]) > 100:
                C[k][index] = C[k][index][:100] + "..."
            if len(C[k][index]) == 0:
                C[k][index] = "Нет данных"
            formatRowTableList.append(C[k][index])
        table.add_row(formatRowTableList)
        formatRowTableList.clear()
print(table)
