import csv
import re
import numpy as np

name = input()

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

if len(B) > 0:
    split = np.array_split(B, len(B) / len(first))

    for arr in split:
        C.append(arr)

    for k in range(0, len(C)):
        for index in range(0, len(first)):
            print(first[index] + ': ' + C[k][index])
        print()
