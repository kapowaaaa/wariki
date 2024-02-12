import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QColor
import random

row = 5
column = 11
balls_field = []
x = 0
y = 0
cell_diameter = 50

for i in range(row):
    row_list = []
    for j in range(column):
        color = random.randint(1, 3)
        cell = [x, y, color]
        x += cell_diameter
        row_list.append(cell)
    balls_field.append(row_list)
    x = 0
    y += cell_diameter

class GameWindow(QMainWindow):
    def __init__(self, row):
        super().__init__()

        self.row = row

        self.setWindowTitle("My Game")
        self.setGeometry(100, 100, 800, 600)

        self.game_field = QLabel(self)
        self.game_field.setGeometry(50, 50, column*cell_diameter, self.row*cell_diameter)
        self.game_field.setStyleSheet("background-color: white; border: 1px solid black;")

        for row in balls_field:
            for cell in row:
                x, y, color = cell
                ball_label = QLabel(self.game_field)
                ball_label.setGeometry(x, y, cell_diameter, cell_diameter)
                ball_label.setStyleSheet(f"background-color: {QColor(color*85, color*85, color*85).name()}; border-radius: {cell_diameter//2}px; border: 1px solid black;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow(row)
    window.show()
    sys.exit(app.exec_())