import csv
import re
import numpy as np

name = input()

A = []
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

# first = (A[0])
# del A[0]

print(first)
print(A)
