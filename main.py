import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
import random

row = 5
column = 11
balls_field = []
x = 0
y = 0
cell_diameter =120

for i in range(row):
    row_list = []
    for j in range(column):
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])  # Randomly choose red, green, or blue
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
        self.shooter_angle = -45

        self.setWindowTitle("Bubble Shooter Game")
        self.setGeometry(0, 0, 1920, 1080)

        self.game_field = QLabel(self)
        self.game_field.setGeometry(50, 50, column*cell_diameter, self.row*cell_diameter)
        self.game_field.setStyleSheet("background-color: white; border: 1px solid black;")

        for row in balls_field:
            for cell in row:
                x, y, color = cell
                ball_label = QLabel(self.game_field)
                ball_label.setGeometry(x, y, cell_diameter, cell_diameter)
                ball_label.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); border-radius: {cell_diameter//2}px; border: 1px solid black;")
                ball_label.color = color

        self.shooter = QLabel(self)
        self.shooter.setGeometry(960 - cell_diameter // 2, 930 - cell_diameter // 2, cell_diameter, cell_diameter)
        self.shooter.setStyleSheet("background-color: gray; border-radius: 45px; border: 1px solid black;")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.gray))
        painter.drawRect(960 - cell_diameter // 4, 930 - cell_diameter // 4, cell_diameter // 2, cell_diameter)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Shoot a random color ball from the shooter
            color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
            ball_label = QLabel(self.game_field)
            ball_label.setGeometry(960 - cell_diameter // 2, 930 - cell_diameter // 2, cell_diameter, cell_diameter)
            ball_label.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); border-radius: {cell_diameter//2}px; border: 1px solid black;")
            ball_label.color = color

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow(row)
    window.show()
    sys.exit(app.exec_())
