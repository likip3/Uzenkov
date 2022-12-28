# print('Введите название вакансии:')
# name = input()
# print('Введите описание вакансии:')
# skills = input()
# print('Введите требуемый опыт работы (лет):')
# skillOp = input()
# print('Введите нижнюю границу оклада вакансии:')
# downEdge = input()
# print('Введите верхнюю границу оклада вакансии:')
# upEdge = input()
# print('Есть ли свободный график (да / нет): ')
# grafik = input()
# print('Является ли данная вакансия премиум-вакансией (да / нет):')
# premium = input()
#
# print('Введите название вакансии: Введите описание вакансии: Введите требуемый опыт работы (лет): Введите нижнюю границу оклада вакансии: Введите верхнюю границу оклада вакансии: Есть ли свободный график (да / нет): Является ли данная вакансия премиум-вакансией (да / нет): ',end=" ")

# grafik = grafik.replace('да','True')
# grafik = grafik.replace("Да","True")
# grafik = grafik.replace("нет","False")
# grafik = grafik.replace("Нет","False")
#
# premium = premium.replace('да','True')
# premium = premium.replace("Да","True")
# premium = premium.replace("нет","False")
# premium = premium.replace("Нет","False")
#
#
#
#
# print(name + type(int(name)))
# print(skills + type(int(skills)))
# print(skillOp + type(int()))
# print(downEdge + type(int(downEdge)))
# print(upEdge + " (int)")
# print(grafik + " (bool)")
# print(premium + " (bool)")
#


name = input()
skills = input()
skillOp = input()
downEdge = input()
upEdge = input()
grafik = input()
premium = input()

grafik = grafik.replace('да', 'True')
grafik = grafik.replace("Да", "True")
grafik = grafik.replace("нет", "False")
grafik = grafik.replace("Нет", "False")

premium = premium.replace('да', 'True')
premium = premium.replace("Да", "True")
premium = premium.replace("нет", "False")
premium = premium.replace("Нет", "False")

print('Введите название вакансии: Введите описание вакансии: Введите требуемый опыт работы (лет): Введите нижнюю границу оклада вакансии: Введите верхнюю границу оклада вакансии: Есть ли свободный график (да / нет): Является ли данная вакансия премиум-вакансией (да / нет): ' +name + ' (' + str(type(name))[8:-2] + ')')
print(skills + ' (' + str(type(skills))[8:-2] + ')')
print(skillOp + ' (' + str(type(int(skillOp)))[8:-2] + ')')
print(downEdge + ' (' + str(type(int(downEdge)))[8:-2] + ')')
print(upEdge + ' (' + str(type(int(downEdge)))[8:-2] + ')')
print(grafik + ' (' + str(type(bool(downEdge)))[8:-2] + ')')
print(premium + ' (' + str(type(bool(downEdge)))[8:-2] + ')')
