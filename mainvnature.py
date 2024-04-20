import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt,QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent


import random
import math

screen_width, screen_height = 0, 0


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        screen_geometry = QApplication.desktop().availableGeometry() # доп шняга добавлена теперь растянуто норм
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setupMediaPlayer()
        
        
        
    

        global screen_width, screen_height
        screen_width = self.size().width()
        screen_height = self.size().height()
        print(screen_width, screen_height)
        self.current_ball = None
        self.shooting_angle = 90
        self.shooting_power = 10
        self.setMouseTracking(True)


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
                ball = [self.x_pos, self.y_pos, color] #хз тут было cell
                balls_field.append(ball)
                self.x_pos += self.ball_size
            if (i + 1) % 2 == 0:  # Проверяем, является ли i+1 последним элементом с четным индексом
                balls_field.pop()  # Удаляем последний элемент из списка balls_field

            self.y_pos += round(self.ball_size / 1.15)

        # self.game_field = QWidget(self)
        # self.game_field.setGeometry(0, 0, column * self.ball_size, total_rows * self.ball_size)
        
        # #создание поля с шариками
        for ball in balls_field:
            
            self.x_pos, self.y_pos, color = ball
            ball_label = QLabel(self)
            ball_label.setGeometry(ball[0], ball[1], self.ball_size, self.ball_size)
            ball_label.setMouseTracking(True)
            ball_label.setStyleSheet(f"background-color: {ball[2]}; "
                                     f"border-radius: {self.ball_size // 2}px; "
                                     f"border: 1px solid black;")
            
            # ball_label.color = color

        self.row = total_rows
        self.shooter_angle = 270 # уголлл

        self.shooter = QLabel(self)
        self.shooter.setGeometry(screen_width // 2 - self.ball_size // 2 - 10, screen_height - self.ball_size*1.5,  # серая херня снизу
                                 100,
                                 100)
        self.shooter.setStyleSheet("background-color: gray; border-radius: 50px; border: 1px solid black;") # настройка цвета и формы серой херни
        
          # Enable mouse tracking

    def paintEvent(self, event): # шутеррррррррррррррррррррррр
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black))
        painter.save()
        painter.translate(self.width() //2,
                         self.height() - self.ball_size // 2) #и эту
        painter.rotate(self.shooter_angle)
        painter.drawRect(-100, -self.ball_size // 4, 100, self.ball_size // 2)
 # эту шляпу надо покадрить
        painter.restore()
        if self.current_ball is not None:
            painter.setBrush(QBrush(QColor(self.current_ball[2])))
            painter.drawEllipse(self.current_ball[0], self.current_ball[1], self.ball_size, self.ball_size)


    def mouseMoveEvent(self, event):
    # Рассчитываем угол относительно центра стрелы и курсора мыши
        dx = event.x() - (self.width() // 2)
        dy = event.y() - (self.height() - self.ball_size)
        self.shooter_angle = math.degrees(math.atan2(-dy, -dx))  # во ;;;;;

        # Обновляем окно для отрисовки нового угла стрелы
        self.update()
        print(f"Mouse move: {event.pos()}")
        print(event.x(), event.y())
    
    def update_shooting_ball(self):
        if self.current_ball is not None:
            dx = math.cos(math.radians(self.shooting_angle)) * self.shooting_power
            dy = math.sin(math.radians(self.shooting_angle)) * self.shooting_power
            self.current_ball[0] += dx
            self.current_ball[1] -= dy
            self.update()



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton : #and self.current_ball is None : 
            self.current_ball = [self.width() // 2 - self.ball_size // 2, self.height() - self.ball_size * 1.5, 'Green']
            # Угол стрельбы должен быть адаптирован для использования в математических расчётах
            self.shooting_angle = self.shooter_angle + 180 if self.shooter_angle < 0 else self.shooter_angle
            self.update()
    
    

    def keyPressEvent(self, event):
        # Объединяем обработку нажатий клавиш
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            self.update_shooting_ball()

    def setupMediaPlayer(self):
        # Инициализация медиаплеера
        self.player = QMediaPlayer()

        # Загрузка файла: укажите правильный путь к файлу
        url = QUrl.fromLocalFile("lalala.mp3")
        content = QMediaContent(url)
        self.player.setMedia(content)

        # Подключение сигнала окончания воспроизведения к слоту для повторного воспроизведения
        self.player.mediaStatusChanged.connect(self.repeatMusic)

        # Начать воспроизведение
        self.player.play()

    def repeatMusic(self, status):
        # Проверка, завершилось ли воспроизведение
        if status == QMediaPlayer.EndOfMedia:
            self.player.play()


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
        self.setStyleSheet('background-color: qlineargradient(spread:reflect, x1:0.506, y1:0.476142, x2:0.506, y2:1, stop:0.0189474 rgba(0, 255, 191, 255), stop:0.76 rgba(0, 137, 123, 255), stop:1 rgba(15, 56, 116, 255));')

        start_button = QPushButton("Начать игру", self)
        start_button.setGeometry(screen_width // 2 - 50, screen_height // 2 + 200, 200, 100)
        start_button.clicked.connect(self.start_game)
        start_button.setStyleSheet ('background-color: qlineargradient(spread:pad, x1:0.512, y1:0, x2:0.517, y2:1, stop:0.00568182 rgba(238, 255, 129, 255), stop:1 rgba(138, 255, 166, 255));font: 75 18pt "Century Schoolbook";border-radius : 50;')

        exit_button = QPushButton("Выйти", self)
        exit_button.setGeometry(0, 0, 150, 50)
        exit_button.clicked.connect(self.close)
        exit_button.setStyleSheet('background-color: qlineargradient(spread:pad, x1:0.512, y1:0, x2:0.517, y2:1, stop:0.00568182 rgba(238, 255, 129, 255), stop:1 rgba(138, 255, 166, 255));font: 75 18pt "Century Schoolbook";border-radius : 25; ')
        
        game_name = QLabel('Шарики', self)
        game_name.setGeometry(screen_width // 2 - 200, screen_height // 2 - 400, 500, 150)
        game_name.setAlignment(Qt.AlignCenter)
        game_name.setStyleSheet('background: transparent;font: 72pt "Century Schoolbook";')
        
        
         
        
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
