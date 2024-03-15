import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
import random
import math

total_rows = 5
column = 15
balls_field = []
x = 0
y = 0

for i in range(total_rows):
    if i % 2 == 0:
        x = 0
    else:
        x = 60
    row_list = []
    for j in range(column):
        color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])  # Randomly choose red, green, or blue
        cell = [x, y, color]
        x += 120
        row_list.append(cell)
    balls_field.append(row_list)
    y += 103

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.row = total_rows
        self.shooter_angle = 180

        self.setWindowTitle("Bubble Shooter Game")
        self.setGeometry(0, 0, 1920, 1080)

        self.game_field = QLabel(self)
        self.game_field.setGeometry(0, 0, column*175, self.row*150)
        self.game_field.setStyleSheet("background-color: white; border: 1px solid black;") #сцена
        self.game_field.setGeometry(0, 0, column * 175, self.row * 150)
        self.game_field.setGeometry(0, 0, 1920, 1080)
        self.game_field.setStyleSheet("background-color: white; border: 1px solid black;")

        for row in balls_field:
            for cell in row:
                x, y, color = cell
                ball_label = QLabel(self.game_field)
                ball_label.setGeometry(x, y, 120, 120)
                ball_label.setStyleSheet(
                    f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); border-radius: {120 // 2}px; border: 1px solid black;")
                ball_label.color = color

        self.shooter = QLabel(self)
        self.shooter.setGeometry(960 - 120 // 2, 930 - 120 // 2, 120, 120)
        self.shooter.setStyleSheet("background-color: gray; border-radius: 45px; border: 1px solid black;")

        self.setMouseTracking(True)  # Enable mouse tracking

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black))
        painter.save()
        painter.translate(self.width() / 2,
                          self.height() - 30)
        painter.rotate(self.shooter_angle)
        painter.drawRect(-15, -60, 30, 60)
        painter.restore()

    def mouseMoveEvent(self, event):
        dx = event.x() - 960
        dy = event.y() - 930
        angle = math.degrees(math.atan2(dy, dx))
        self.shooter_angle = angle
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
            ball_label = QLabel(self.game_field)
            ball_label.setGeometry(960 - 120 // 2, 930 - 120 // 2, 120, 120)
            ball_label.setStyleSheet(
                f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); border-radius: {120 // 2}px; border: 1px solid black;")
            ball_label.color = color

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Bubble Shooter Game")
        self.setGeometry(0, 0, 1920, 1080)

        start_button = QPushButton("Начать игру", self)
        start_button.setGeometry(960, 540, 100, 50)
        start_button.clicked.connect(self.start_game)

        exit_button = QPushButton("Выйти", self)
        exit_button.setGeometry(0, 0, 100, 50)
        exit_button.clicked.connect(self.close)

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.show()
    sys.exit(app.exec_())

