name = input()
skills = input()
skillOp = input()
downEdge = input()
upEdge = input()
grafik = input()
premium = input()

middleedge = int((int(downEdge)+int(upEdge))/2)

if skillOp[len(skillOp)-1] == "1":
    postYear = " год"
elif skillOp[len(skillOp)-1] == "2" or skillOp[len(skillOp)-1] == "3" or skillOp[len(skillOp)-1] == "4":
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

print('Введите название вакансии: Введите описание вакансии: Введите требуемый опыт работы (лет): Введите нижнюю границу оклада вакансии: Введите верхнюю границу оклада вакансии: Есть ли свободный график (да / нет): Является ли данная вакансия премиум-вакансией (да / нет): ' +name)
print("Описание: "+skills)
print("Требуемый опыт работы: "+skillOp + postYear)
print("Средний оклад: "+ str(middleedge) + postPrice)
print("Свободный график: "+grafik)
print("Премиум-вакансия: "+premium)
