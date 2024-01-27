import random

row = 5
column = 10
cell = 0
field = []

for i in range(row):
    for j in range(column):
        cell = random.randint(1, 3)
        field.append(cell)
    print(field)
    field = []

