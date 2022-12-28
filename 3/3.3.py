import csv
import re
from prettytable import PrettyTable
from textwrap import fill

# name = input()
name = 'vacancies.csv'


#
# def array_split(ary, indices_or_sections, axis=0):
#     sub_arys = []
#     sary = _nx.swapaxes(ary, axis, 0)
#     for i in range(Nsections):
#         st = div_points[i]
#         end = div_points[i + 1]
#         sub_arys.append(_nx.swapaxes(sary[st:end], axis, 0))
#
#     return sub_arys

def equal_array_split(arr, split_arr_len_float):
    split_arr_len = int(split_arr_len_float)
    array_length = len(arr)
    if array_length % split_arr_len == 0:
        return [arr[i:i+split_arr_len]
                for i in range(0,array_length,split_arr_len)]
    else:
        return "Invalid split array length!!"

A = []
B = []
C = []

table = PrettyTable(hrules=1, align="l")

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

table.field_names = ["№"] + first

repDict = {"noExperience": "Нет опыта", "between1And3": "От 1 года до 3 лет", "between3And6": "От 3 до 6 лет",
           "moreThan6": "Более 6 лет", "AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро",
           "GEL": "Грузинский лари", "KGS": "Киргизский сом",
           "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум", "True": "Да",
           "False": "Нет"
           }

if len(B) > 0:
    split = equal_array_split(B, len(B) / len(first))

    for arr in split:
        C.append(arr)

    for k in range(0, len(C)):
        for index in range(0, len(first)):
            # if index == 4 or index == 8 or index == 9 or index == 3:
            for word, initial in repDict.items():
                if C[k][index] == word:
                    C[k][index] = initial
            if index != 2:
                C[k][index] = fill(C[k][index], width=20)
            else:
                C[k][index] = C[k][index].replace(", ", "\n")

            if len(C[k][index]) > 100:
                C[k][index] = C[k][index][0:100] + '...'
            # C[k][2] = C[k][index].replace(',', '\n')

        table.add_row([k] + C[k])
        # print(first[index] + ': ' + C[k][index])
print(table)



