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
        screen_geometry = QApplication.desktop().availableGeometry() # доп шняга добавлена теперь растянуто норм
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        
    

        global screen_width, screen_height
        screen_width = self.size().width()
        screen_height = self.size().height()
        print(screen_width, screen_height)
        self.current_ball = None
        self.shooting_angle = 90
        self.shooting_power = 10


        self.setWindowTitle("Шарики")
        # self.setGeometry(0, 0, screen_width, screen_height)

        total_rows = 8
        column = 25
        balls_field = []

        self.x_pos = 0
        self.y_pos = 0
        global ball_size
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
            if (i + 1) % 2 == 0:  # Проверяем, является ли i+1 последним элементом с четным индексом
                balls_field.pop()  # Удаляем последний элемент из списка balls_field

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

        self.row = total_rows
        self.shooter_angle = 270 # уголлл

        self.shooter = QLabel(self)
        self.shooter.setGeometry(screen_width // 2 - self.ball_size // 2, screen_height - self.ball_size*1.5,  # серая херня снизу
                                 100,
                                 100)
        self.shooter.setStyleSheet("background-color: gray; border-radius: 50px; border: 1px solid black;") # настройка цвета и формы серой херни
        
        self.setMouseTracking(True)  # Enable mouse tracking

    def paintEvent(self, event): # шутеррррррррррррррррррррррр
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black))
        painter.save()
        painter.translate(self.width() //2,
                          self.height() - self.ball_size)
        painter.rotate(self.shooter_angle)
        painter.drawRect(-2, -self.ball_size // 2, 100, self.ball_size//2)
        painter.restore()
        if self.current_ball is not None:
            painter.setBrush(QBrush(QColor(self.current_ball[2])))
            painter.drawEllipse(self.current_ball[0], self.current_ball[1], self.ball_size, self.ball_size)


    def mouseMoveEvent(self, event):
    # Рассчитываем угол относительно центра стрелы и курсора мыши
        dx = event.x() - (self.width() // 2)
        dy = event.y() - (self.height() - self.ball_size)
        self.shooter_angle = math.degrees(math.atan2(-dy, dx))  # Угол поворота должен быть отрицательным по оси Y

        # Обновляем окно для отрисовки нового угла стрелы
        self.update()
        print(f"Mouse move: {event.pos()}")
    
    def update_shooting_ball(self):
        if self.current_ball is not None:
            dx = math.cos(math.radians(self.shooting_angle)) * self.shooting_power
            dy = math.sin(math.radians(self.shooting_angle)) * self.shooting_power
            self.current_ball[0] += dx
            self.current_ball[1] -= dy
            self.update()



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_ball is None:
            self.current_ball = [self.width() // 2 - self.ball_size // 2, self.height() - self.ball_size * 1.5, 'blue']
            # Угол стрельбы должен быть адаптирован для использования в математических расчётах
            self.shooting_angle = self.shooter_angle + 180 if self.shooter_angle < 0 else self.shooter_angle
            self.update()
    
    

    def keyPressEvent(self, event):
        # Объединяем обработку нажатий клавиш
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            self.update_shooting_ball()



class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_window = None

        global screen_width, screen_height
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height() # поменял, тепреь растягивается норсм но код не рабоатет
        
        self.setWindowTitle("Шарики")
        self.setGeometry(0, 0, screen_width, screen_height)

        start_button = QPushButton("Start game", self)
        start_button.setGeometry(screen_width // 2 - 50, screen_height // 2 + 200, 200, 100)
        start_button.clicked.connect(self.start_game)
        start_button.setStyleSheet ('background-color: qlineargradient(spread:pad, x1:0.5, y1:0.0397727, x2:0.886364, y2:1, stop:0.0852273 rgba(185, 255, 118, 241), stop:1 rgba(255, 255, 255, 255));font: 18pt "Old English Text MT";border-radius : 50;')

        exit_button = QPushButton("Exit", self)
        exit_button.setGeometry(0, 0, 150, 50)
        exit_button.clicked.connect(self.close)
        exit_button.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0.931727, y1:0.96, x2:0.0340909, y2:0, stop:0.0852273 rgba(126, 255, 3, 241), stop:1 rgba(255, 255, 255, 255));font: 18pt "Old English Text MT";border-radius : 25;')
        
        game_name = QLabel('Шарики', self)
        
    def start_game(self):
        self.game_window = GameWindow()
        # self.game_window.setGeometry(0, 0, screen_width, screen_height)
        # self.game_window.ball_size = min(screen_width // self.game_window.total_rows, screen_height // self.game_window.column)
        # self.game_window.shooter.setGeometry(screen_width // 2 - self.game_window.ball_size // 2,
        #                                      screen_height - self.game_window.ball_size // 2,
        #                                      self.game_window.ball_size // 2, self.game_window.ball_size // 2)

        self.close()


        self.game_window.showMaximized()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.showMaximized()
    sys.exit(app.exec_())
