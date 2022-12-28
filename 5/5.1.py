import csv
import re
import sys
from var_dump import var_dump
from prettytable import PrettyTable

# region Словари
repDict = {
    'Название': 'name',
    'Описание': 'description',
    'Навыки': 'key_skills',
    'Оклад': 'salary_average',
    'Опыт работы': 'experience_id',
    'Идентификатор валюты оклада': 'salary_currency',
    'Дата публикации вакансии': 'published',
    'Премиум-вакансия': 'premium',
    'Название региона': 'area_name',
    'Компания': 'employer_name',
}

expRep = {
    'noExperience': 'Нет опыта',
    'between1And3': 'От 1 года до 3 лет',
    'between3And6': 'От 3 до 6 лет',
    'moreThan6': 'Более 6 лет',
}

expSort = {
    'Нет опыта': 1,
    'От 1 года до 3 лет': 2,
    'От 3 до 6 лет': 3,
    'Более 6 лет': 4
}

salRep = {
    'AZN': 'Манаты',
    'BYR': 'Белорусские рубли',
    'EUR': 'Евро',
    'GEL': 'Грузинский лари',
    'KGS': 'Киргизский сом',
    'KZT': 'Тенге',
    'RUR': 'Рубли',
    'UAH': 'Гривны',
    'USD': 'Доллары',
    'UZS': 'Узбекский сум'
}

headers = ['name', 'description', 'key_skills', 'experience_id', 'premium', 'employer_name', 'salary', 'area_name',
           'published_at']
RUHeaders = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад',
             'Название региона', 'Дата публикации вакансии']

currencyTransfer = {
    'AZN': 35.68,
    'BYR': 23.91,
    'EUR': 59.90,
    'GEL': 21.74,
    'KGS': 0.76,
    'KZT': 0.13,
    'RUR': 1,
    'UAH': 1.64,
    'USD': 60.66,
    'UZS': 0.0055,
}
# endregion
# region Лямбды
formatter = dict(name=lambda a: re.sub('Stack.*разработч', 'Stack разработч', a),
                 description=lambda a: Reduction(ClearTable(a)), key_skills=lambda a: Reduction(a),
                 experience_id=lambda a: expRep[a], premium=lambda a: 'Да' if a.lower() == 'true' else 'Нет',
                 employer_name=lambda a: a, area_name=lambda a: a, salary_from=lambda a: int(float(a)),
                 salary_to=lambda a: int(float(a)), salary_currency=lambda a: a,
                 salary_gross=lambda a: 'Без вычета налогов' if a.lower() == 'true' else 'С вычетом налогов',
                 salary=lambda a: '{0} - {1} ({2}) ({3})'.format(Separator(a['salary_from']), Separator(a['salary_to']),
                                                                 salRep[a['salary_currency']],
                                                                 a['salary_gross']),
                 salary_average=lambda a: currencyTransfer[a['salary_currency']] * (
                         (a['salary_from'] + a['salary_to']) / 2),
                 published_at=lambda a: '{0[2]}.{0[1]}.{0[0]}'.format(a[:10].split('-')))

SortLambdas = {
    'Название': lambda a, b: b['name'] == a,
    'Идентификатор валюты оклада': lambda a, b: salRep[b['salary_currency']] == a,
    'Навыки': lambda a, b: all([x in b['skills'] for x in a.split(', ')]),
    'Оклад': lambda a, b: b['salary_from'] <= float(a) <= b['salary_to'],
    'Опыт работы': lambda a, b: b['experience_id'] == a,
    "Премиум-вакансия": lambda a, b: b['premium'] == a,
    'Название региона': lambda a, b: b['area_name'] == a,
    'Компания': lambda a, b: b['employer_name'] == a,
    'Дата публикации вакансии': lambda a, b: b['published_at'] == a
}


# endregion
# region Функции
def PrintResult(vacancies):
    vacanciesTemp = []
    length = len(listSalFromTo)
    InputFilter(vacancies)
    if sortInp:
        vacancies = filter(lambda a: SortLambdas[sortInp[0]](sortInp[1], a), vacancies)
    for index, vacancy in enumerate(vacancies):
        if (length > 1 and listSalFromTo[0] <= index < listSalFromTo[1]) or (
                length == 1 and listSalFromTo[0] <= index) or length == 0:
            vacanciesTemp.append([index + 1] + [vacancy[key] for key in headers])

    if len(vacanciesTemp) == 0:
        print('Ничего не найдено')
        sys.exit()
    table = PrettyTable(align='l', field_names=RUHeaders, max_width=20, hrules=1)
    table.add_rows(vacanciesTemp)
    var_dump(table)
    # print(table.get_string(fields=columnsList))


def InputFilter(vacancies):
    if filterInp != '':
        if filterInp == 'Опыт работы':
            vacancies.sort(key=lambda a: expSort[a[repDict[filterInp]]], reverse=reversInp)
        elif filterInp == 'Навыки':
            vacancies.sort(key=lambda a: len(a['skills']), reverse=reversInp)
        else:
            vacancies.sort(key=lambda a: a[repDict[filterInp]], reverse=reversInp)
    elif filterInp == '' and reversInp:
        vacancies.reverse()


def ClearTable(string):
    result = re.sub(r'<.*?>', '', string)
    result = re.sub(r'\s+', ' ', result)
    return result.strip()


def Separator(number):
    return '{:,}'.format(number).replace(',', ' ')


def Reduction(string):
    return string if len(string) <= 100 else string[:100] + '...'


def FiltrFile(csvHeader, csvRows):
    dataVacancies = []
    for csvRow in csvRows:
        tempDict = {}
        for key, value in zip(csvHeader, csvRow):
            if key == 'published_at':
                tempDict['published'] = value
            elif key == 'key_skills':
                tempDict['skills'] = value.split('\n')
            tempDict[key] = formatter[key](value)
        tempDict['salary_average'] = formatter['salary_average'](tempDict)
        tempDict['salary'] = formatter['salary'](tempDict)
        dataVacancies.append(tempDict)
    return dataVacancies


def CSVReader(filename):
    csvRows = []
    csvHeader = []
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        for index, row in enumerate(reader):
            if index == 0:
                csvHeader = row
                length = len(row)
            else:
                if '' not in row and len(row) == length:
                    csvRows.append(row)
    return csvHeader, csvRows


# endregion

# filenameInp = 'vacancies_medium.csv'
filenameInp = input('Введите название файла: ')
sortInp = str(input('Введите параметр фильтрации: ')).strip()
filterInp = str(input('Введите параметр сортировки: ')).strip()
reversInp = str(input('Обратный порядок сортировки (Да / Нет): ')).strip()
elementFromToInp = input('Введите диапазон вывода: ')
columnsInp = input('Введите требуемые столбцы: ')

if sortInp != '':
    if ': ' not in sortInp:
        sortInp = True
    else:
        sortInp = sortInp.split(': ')
        sortInp = (sortInp[0], sortInp[1])
        if sortInp[0] not in list(SortLambdas.keys()):
            sortInp = False
else:
    sortInp = ()

order_error = reversInp not in ['', 'Да', 'Нет']
reversInp = True if reversInp == 'Да' else False

listSalFromTo = [] if elementFromToInp == '' else [int(a) - 1 for a in elementFromToInp.split()]
columnsList = RUHeaders if columnsInp == '' else ['№'] + [a for a in columnsInp.split(', ') if a in RUHeaders]

if isinstance(sortInp, bool):
    if sortInp:
        print('Формат ввода некорректен')
    else:
        print('Параметр поиска некорректен')
    sys.exit()
if filterInp != '' and filterInp not in RUHeaders:
    print('Параметр сортировки некорректен')
    sys.exit()
if order_error:
    print('Порядок сортировки задан некорректно')
    sys.exit()

header, rows = CSVReader(filenameInp)

if len(rows) == 0:
    if len(header) == 0:
        print('Пустой файл')
    else:
        print('Нет данных')
    sys.exit()
all_vacancies = FiltrFile(header, rows)
PrintResult(all_vacancies)
