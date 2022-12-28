import csv
import re
import sys

from prettytable import PrettyTable

# region Словари
replacements = {
    "name": "Название",
    "description": "Описание",
    "key_skills": "Навыки",
    "experience_id": "Опыт работы",
    "premium": "Премиум-вакансия",
    "employer_name": "Компания",
    "salary_from": "Нижняя граница вилки оклада",
    "salary_to": "Верхняя граница вилки оклада",
    "salary_gross": "Оклад указан до вычета налогов",
    "salary_currency": "Идентификатор валюты оклада",
    "area_name": "Название региона",
    "published_at": "Дата публикации вакансии",
}
repDict = {
    "noExperience": "Нет опыта",
    "between1And3": "От 1 года до 3 лет",
    "between3And6": "От 3 до 6 лет",
    "moreThan6": "Более 6 лет",
    "AZN": "Манаты",
    "BYR": "Белорусские рубли",
    "EUR": "Евро",
    "GEL": "Грузинский лари",
    "KGS": "Киргизский сом",
    "KZT": "Тенге",
    "RUR": "Рубли",
    "UAH": "Гривны",
    "USD": "Доллары",
    "UZS": "Узбекский сум",
    "True": "Да",
    "False": "Нет",
}
allFields = [
    "№",
    "Название",
    "Описание",
    "Навыки",
    "Опыт работы",
    "Премиум-вакансия",
    "Компания",
    "Оклад",
    "Название региона",
    "Дата публикации вакансии",
]
simpleFiltersDict = {
    "Название",
    "Описание",
    "Компания",
    "Дата публикации вакансии",
    "Название региона",
    "Идентификатор валюты оклада",
    "Премиум-вакансия",
    "Опыт работы"
}
advFiltersDict = {
    "Навыки",
    "Оклад"
}
# endregion
# region Переменные
A = []
B = []
C = []
first = None
tempSum = 0
formatRowTableList = []
countNum = 0
isReversedSort = None
# endregion
# region Функции
def insert(source_str, insert_str, pos):
    return source_str[:pos] + insert_str + source_str[pos:]


def split_equal(lst):
    len_ = len(lst)
    subLen = 12
    return [lst[splitI: splitI + subLen] for splitI in range(0, len_, subLen)]


def simpleAllow(rowToFilter):
    return rowToFilter[filterIdx].lstrip().rstrip() == tableFilter[1].lstrip().rstrip()


def salaryAllow(salFromF, salToF):
    return int(salFromF.partition(".")[0]) <= int(tableFilter[1]) <= int(salToF.partition(".")[0])


def skillsAllow(rowSkills):
    skillsRowList = []
    for q in tableFilter[1].split(','):
        skillsRowList.append(q.lstrip().rstrip())

    for skillF in skillsRowList:
        if -1 == rowSkills.find(skillF):
            return False
    return True


# endregion

name = input("Введите название файла:")
# name = 'vacancies_medium.csv'

tableFilter = input("Введите параметр фильтрации:").split(': ')
tableSortBy = input("Введите параметр сортировки:")
reversedSortInput = input("Обратный порядок сортировки (Да / Нет):")
elementFromTo = input("Введите диапазон вывода:").split(" ")
categories = input("Введите требуемые столбцы:").split(", ")

if reversedSortInput == "Да":
    isReversedSort = True

if not (len(tableFilter) == 1 and len(tableFilter[0]) == 0) and not (tableFilter[0] in simpleFiltersDict or tableFilter[0] in advFiltersDict):
    print("Параметр поиска некорректен")
    sys.exit()

with open(name, encoding="utf-8-sig") as f:
    tab = csv.reader(f)
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
    if first is None:
        print("Пустой файл")
        sys.exit()
    if len(A) == 0:
        print("Нет данных")
        sys.exit()

# region indexes
nameIdx = first.index("name")
descIdx = first.index("description")
skillsIdx = first.index("key_skills")
premiumIdx = first.index("premium")
companyIdx = first.index("employer_name")
sFromIdx = first.index("salary_from")
sToIdx = first.index("salary_to")
currIdx = first.index("salary_currency")
areaIdx = first.index("area_name")
# endregion

for x in A:
    for i in x:
        i = re.sub(r"<[^<>]*>", "", i)
        i = re.sub(r"\n", ", ", i)
        i = str.strip(re.sub(r"\s+", " ", i))
        B.append(i)

replacer = replacements.get
first = [replacer(n, n) for n in first]

if len(tableFilter) == 2:
    filterIdx = first.index(tableFilter[0])

table = PrettyTable(hrules=1, align="l")
table.field_names = allFields
table.max_width = 20

if len(B) > 0:
    split = split_equal(B)
    for arr in split:
        C.append(arr)

    for k in range(0, len(C)):
        formatRowTableList.append(str(k + 1))
        for index in range(0, len(first)):
            if index == 6 or index == 7:
                tempSum = tempSum + int(C[k][index].partition(".")[0])  # Средний оклад сумма
                continue

            for word, initial in repDict.items():  # Стаж валюта булевы
                if C[k][index] == word:
                    C[k][index] = initial

            if index == 8:
                if C[k][index] == "Нет":
                    C[k][index] = "С вычетом налогов"
                if C[k][index] == "Да":
                    C[k][index] = "Без вычета налогов"
                continue

            if index == 11:
                C[k][index] = (
                        C[k][index][8:10] + "." + C[k][index][5:7] + "." + C[k][index][0:4]  # дата время
                )

            if index == 9:  # особый вывод оклада
                formatRowTableList.append(
                    "{0:,}".format(int(C[k][6].partition(".")[0])).replace(",", " ")
                    + " - "
                    + "{0:,}".format(int(C[k][7].partition(".")[0])).replace(",", " ")
                    + " ("
                    + C[k][index]
                    + ")"
                    + " ("
                    + C[k][index - 1]
                    + ")"
                )
                tempSum = 0
                continue

            if index == 2:  # новая строка к скилам
                C[k][index] = C[k][index].replace(", ", "\n")

            if len(C[k][index]) > 100:  # обрезка
                C[k][index] = C[k][index][:100] + "..."

            formatRowTableList.append(C[k][index])  # стандартный вывод
        if (len(tableFilter) == 1 and len(tableFilter[0]) == 0) or \
            (tableFilter[0] in simpleFiltersDict and simpleAllow(C[k])) or \
            (tableFilter[0] == "Оклад" and salaryAllow(C[k][sFromIdx], C[k][sToIdx])) or \
            (tableFilter[0] == "Навыки" and skillsAllow(formatRowTableList[3])):
            countNum = countNum + 1
            formatRowTableList[0] = countNum
            table.add_row(formatRowTableList)

        formatRowTableList.clear()
if countNum == 0:
    print("Ничего не найдено")
    sys.exit()

if len(categories) == 1 and len(categories[0]) == 0:
    categories = allFields
if len(elementFromTo) == 1 and len(elementFromTo[0]) == 0:
    print(table.get_string(fields=["№"] + categories))
elif len(elementFromTo) == 2:
    print(table.get_string(fields=["№"] + categories, start=int(elementFromTo[0]) - 1, end=int(elementFromTo[1]) - 1))
else:
    print(table.get_string(fields=["№"] + categories, start=int(elementFromTo[0]) - 1))
