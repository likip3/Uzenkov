def input_text_data(inp_test):
    while True:
        text = input(inp_test)
        if len(text) == 0:
            print('Данные некорректны, повторите ввод')
        else:
            return text


def input_num_data(inp_test):
    while True:
        num = input(inp_test)
        if not num.isnumeric():
            print('Данные некорректны, повторите ввод')
        else:
            return num


def input_bool_data(inp_test):
    while True:
        num = input(inp_test)
        if not (num == "да" or num == "нет"):
            print('Данные некорректны, повторите ввод')
        else:
            return num


name = input_text_data("Введите название вакансии: ")
skills = input_text_data("Введите описание вакансии: ")
skillOp = input_num_data("Введите требуемый опыт работы (лет): ")
downEdge = input_num_data("Введите нижнюю границу оклада вакансии: ")
upEdge = input_num_data("Введите верхнюю границу оклада вакансии: ")
grafik = input_bool_data("Есть ли свободный график (да / нет): ")
premium = input_bool_data("Является ли данная вакансия премиум-вакансией (да / нет): ")

middleedge = int((int(downEdge) + int(upEdge)) / 2)

if skillOp[len(skillOp) - 1] == "1":
    postYear = " год"
elif skillOp[len(skillOp) - 1] == "2" or skillOp[len(skillOp) - 1] == "3" or skillOp[len(skillOp) - 1] == "4":
    postYear = " года"
else:
    postYear = " лет"

if 11 <= middleedge % 100 <= 19:
    postPrice = ' рублей'
else:
    n1 = middleedge % 10
    if n1 == 0 or 5 <= n1 <= 9:
        postPrice = ' рублей'
    elif n1 == 1:
        postPrice = ' рубль'
    elif 2 <= n1 <= 4:
        postPrice = ' рубля'

print(name)
print("Описание: " + skills)
print("Требуемый опыт работы: " + skillOp + postYear)
print("Средний оклад: " + str(middleedge) + postPrice)
print("Свободный график: " + grafik)
print("Премиум-вакансия: " + premium)
