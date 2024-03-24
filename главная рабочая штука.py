import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt
import random
import math

screen_width, screen_height = 0, 0


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        global screen_width, screen_height
        screen_width = self.size().width()
        screen_height = self.size().height()
        print(screen_width, screen_height)

        self.setWindowTitle("Bubble Shooter Game")
        # self.setGeometry(0, 0, screen_width, screen_height)

        total_rows = 5
        column = 16
        balls_field = []

        self.x_pos = 0
        self.y_pos = 0

        self.ball_size = min(screen_width // column, screen_width // column)

        for i in range(total_rows):
            if i % 2 == 0:
                self.x_pos = 0
            else:
                self.x_pos = self.ball_size // 2
            for j in range(column):
                # color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])  # Randomly choose red, green, or blue
                color = random.choice(['red', 'green', 'blue'])  # Randomly choose red, green, or blue
                cell = [self.x_pos, self.y_pos, color]
                balls_field.append(cell)
                self.x_pos += self.ball_size
            self.y_pos += round(self.ball_size / 1.15)

        self.game_field = QLabel(self)
        self.game_field.setGeometry(0, 0, column * self.ball_size, total_rows * self.ball_size)

        for ball in balls_field:
            self.x_pos, self.y_pos, color = ball
            ball_label = QLabel(self.game_field)
            ball_label.setGeometry(ball[0], ball[1], self.ball_size, self.ball_size)
            ball_label.setStyleSheet(f"background-color: {ball[2]}; "
                                     f"border-radius: {self.ball_size // 2}px; "
                                     f"border: 1px solid black;")
            # ball_label.color = color

        # self.row = total_rows
        # self.shooter_angle = 180

        # self.shooter = QLabel(self)
        # self.shooter.setGeometry(screen_width // 2 - self.ball_size // 2, screen_height - self.ball_size // 2,
        #                          self.ball_size // 2,
        #                          self.ball_size // 2)
        # self.shooter.setStyleSheet("background-color: gray; border-radius: 45px; border: 1px solid black;")
        #
        # self.setMouseTracking(True)  # Enable mouse tracking

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.setPen(Qt.black)
    #     painter.setBrush(QBrush(Qt.black))
    #     painter.save()
    #     painter.translate(self.width() / 2,
    #                       self.height() - self.ball_size // 2)
    #     painter.rotate(self.shooter_angle)
    #     painter.drawRect(-10, -self.ball_size // 2, 30, self.ball_size)
    #     painter.restore()

    # def mouseMoveEvent(self, event):
    #     dx = event.x() - screen_width // 2
    #     dy = event.y() - screen_height
    #     angle = math.degrees(math.atan2(dy, dx))
    #     self.shooter_angle = angle
    #     self.update()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
    #         ball_label = QLabel(self.game_field)
    #         ball_label.setGeometry(screen_width // 2 - self.ball_size // 2,
    #                                screen_height - self.ball_size // 2, self.ball_size,
    #                                self.ball_size)
    #         ball_label.setStyleSheet(f"background-color: rgb({color[0]}, {color[1]}, {color[2]}); "
    #                                  f"border-radius: {self.ball_size // 2}px; "
    #                                  f"border: 1px solid black;")
    #         ball_label.color = color

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_window = None

        global screen_width, screen_height


        screen_geometry = QApplication.desktop().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height() # поменял, тепреь растягивается норсм но код не рабоатет

        screen_width = self.size().width()
        screen_height = self.size().height()


        self.setWindowTitle("Bubble Shooter Game")
        # self.setGeometry(0, 0, screen_width, screen_height)

        start_button = QPushButton("Начать игру", self)
        start_button.setGeometry(screen_width // 2 - 50, screen_height // 2 - 25, 100, 50)
        start_button.clicked.connect(self.start_game)

        exit_button = QPushButton("Выйти", self)
        exit_button.setGeometry(0, 0, 100, 50)
        exit_button.clicked.connect(self.close)

    def start_game(self):
        #self.game_window = GameWindow()
        self.game_window.setGeometry(0, 0, screen_width, screen_height)
        self.game_window.ball_size = min(screen_width // self.game_window.row, screen_height // self.game_window.column)
        self.game_window.shooter.setGeometry(screen_width // 2 - self.game_window.ball_size // 2,
                                             screen_height - self.game_window.ball_size // 2,
                                             self.game_window.ball_size // 2, self.game_window.ball_size // 2)

        self.close()


        # self.game_window.showMaximized()

        self.game_window = GameWindow()
        self.game_window.showMaximized()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_window = GameWindow()
    start_window.showMaximized()
    sys.exit(app.exec_())
