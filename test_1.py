import random

row = 5
column = 11
cell = []
balls_field = []
x = 0
y = 0

for i in range(row):
    row_list = []
    for j in range(column):
        color = random.randint(1, 3)
        cell = [x, y, color]
        x += 200
        row_list.append(cell)
    print(row_list)
    x = 0
    y += 200
    balls_field.append(row_list)

# print(balls_field)

