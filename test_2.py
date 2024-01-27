import random

row = 5
column = 11
cell = 0
balls_field = []

for i in range(row):
    row_list = []
    for j in range(column):
        cell = random.randint(1, 3)
        row_list.append(cell)
    balls_field.append(row_list)

print(balls_field)
