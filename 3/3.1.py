import csv
import re
import numpy as np

name = input()
# name = 'vacancies_medium.csv'

A = []
B = []
C = []

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
        if len(row) == len(first):
            A.append(row)

for x in A:
    for i in x:
        i = re.sub(r'<[^<>]*>', '', i)
        i = re.sub(r'\n', ', ', i)
        i = str.strip(re.sub(r'\s+', ' ', i))
        B.append(i)

replacements = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
                'premium': 'Премиум-вакансия', 'employer_name': 'Компания',
                'salary_from': 'Нижняя граница вилки оклада', 'salary_to': 'Верхняя граница вилки оклада',
                'salary_gross': 'Оклад указан до вычета налогов', 'salary_currency': 'Идентификатор валюты оклада',
                'area_name': 'Название региона', 'published_at': 'Дата и время публикации вакансии'
                }
replacer = replacements.get
first = [replacer(n, n) for n in first]

repDict = {"True":"Да", "False": "Нет"}

if len(B) > 0:
    split = np.array_split(B, len(B) / len(first))

    for arr in split:
        C.append(arr)

    for k in range(0, len(C)):
        for index in range(0, len(first)):
            if index == 4 or index == 8 or index == 9 or index == 3:
                for word, initial in repDict.items():
                    if C[k][index] == word:
                        C[k][index] = initial
            print(first[index] + ': ' + C[k][index])
        print()
