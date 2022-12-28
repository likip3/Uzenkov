import csv
import re
import numpy as np

name = input()
# name = 'vacancies_medium.csv'

A = []
B = []
C = []
first = None
temp = 0


# region funk
def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


def ReformatFile():
    global i
    for x in A:
        for i in x:
            i = re.sub(r'<[^<>]*>', '', i)
            i = re.sub(r'\n', ', ', i)
            i = str.strip(re.sub(r'\s+', ' ', i))
            B.append(i)


def ConvertTax():
    if C[k][index] == "Нет":
        C[k][index] = "С вычетом налогов"
    if C[k][index] == "Да":
        C[k][index] = "Без вычета налогов"


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

# region dict
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

with open(name, encoding='utf-8-sig') as f:
    tab = csv.reader(f)
    AllowRows()
ReformatFile()
replacer = replacements.get
first = [replacer(n, n) for n in first]

if len(B) > 0:
    split = np.array_split(B, len(B) / len(first))

    for arr in split:
        C.append(arr.tolist())

    for k in range(0, len(C)):
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
                print(first[index - 1][0:5] + ': ' + '{0:,}'.format(int(C[k][6].partition('.')[0])).replace(',',
                                                                                                            ' ') + ' - ' + '{0:,}'.format(
                    int(C[k][7].partition('.')[0])).replace(',', ' ') + ' (' + C[k][index] + ')' + ' (' + C[k][
                          index - 1] + ')')
                temp = 0
                continue
            print(first[index] + ': ' + C[k][index])
        print()
