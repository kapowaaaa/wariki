import random

pole=[[0] * 5 for _ in range(5)]
for i in range(5):
    for j in range(5):
        pole[i][j] = random.randint(1, 3)
for row in pole:
    print(row)