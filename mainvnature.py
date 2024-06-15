import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

import random
import math

screen_width, screen_height = 0, 0
shooter_angle = 90

def get_random_color():
    # Список возможных именованных цветов
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink']
    return random.choice(colors)
    
class EndGame(QMainWindow):
    def __init__(self, scr, gmvr):
        super().__init__()
        self.gameover = gmvr
        self.score = scr
        screen_geometry = QApplication.desktop().availableGeometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0.767, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 47, 255), stop:1 rgba(21, 21, 21, 255))')
        if self.gameover == 0:
            res = QLabel('Проигрыш', self)
        else:
            res = QLabel('Выигрыш', self)
        res.setGeometry(screen_width // 2 - 200, screen_height // 2 - 400, 500, 150)
        res.setAlignment(Qt.AlignCenter)
        res.setStyleSheet('background: transparent;font: 72pt "Century Schoolbook";color: rgb(255, 255, 255);')
        score_l = QLabel('Очки: '+str(self.score), self)
        score_l.setGeometry(screen_width // 2 - 200, screen_height // 2 - 100, 500, 150)
        score_l.setAlignment(Qt.AlignCenter)
        score_l.setStyleSheet('background: transparent;font: 72pt "Century Schoolbook";color: rgb(255, 255, 255);')
        
        exit_button = QPushButton("Выйти", self)
        exit_button.setGeometry(0, 0, 150, 50)
        exit_button.clicked.connect(self.close)
        exit_button.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.494318, y2:0.926, stop:0 rgba(0, 0, 214, 255), stop:0.897727 rgba(24, 15, 122, 255)) ;font: 75 18pt "Century Schoolbook";border-radius : 25;color: rgb(255, 255, 255); ')
        
        start_button = QPushButton("Играть ещё раз", self)
        start_button.setGeometry(screen_width // 2 - 50, screen_height // 2 + 200, 200, 100)
        start_button.clicked.connect(self.start_game)
        start_button.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.494318, y2:0.926, stop:0 rgba(0, 0, 214, 255), stop:0.897727 rgba(24, 15, 122, 255));font: 75 18pt "Century Schoolbook";border-radius : 50;color: rgb(255, 255, 255);')
    
    def start_game(self):
        self.game_window = GameWindow()
        self.close()
        self.game_window.showMaximized()

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = None
        screen_geometry = QApplication.desktop().availableGeometry()  # доп шняга добавлена теперь растянуто норм
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())
        self.setupMediaPlayer()
        self.timer_num = 0
        self.num_step = 0

        global screen_width, screen_height
        screen_width = self.size().width()
        screen_height = self.size().height()
        print(screen_width, screen_height)
        self.current_ball = None
        self.shooting_angle = 90  # угол шара
        self.shooting_power = 15  # по сути - это шаг, с которым передвигается стреляющий шар
        self.setMouseTracking(True)
        self.can_checking = True

        self.setWindowTitle("Шарики")

        total_rows = 8
        self.column = 25
        self.balls_field = []

        self.x_pos = 0
        self.y_pos = 0
        self.ball_size = min(screen_width // self.column, screen_width // self.column)
        print(self.ball_size)

        for i in range(total_rows):
            if i % 2 == 0:
                self.x_pos = 0
            else:
                self.x_pos = self.ball_size // 2
            for j in range(self.column):
                color = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink'])  # Randomly choose red, green, or blue
                ball = [self.x_pos, self.y_pos, color, QLabel(self)]
                self.balls_field.append(ball)
                self.x_pos += self.ball_size
            if (i + 1) % 2 == 0:  # Проверяем, является ли i+1 последним элементом с четным индексом
                self.balls_field.pop()  # Удаляем последний элемент из списка balls_field

            self.y_pos += round(self.ball_size * math.sin(math.radians(60)))

        for ball in self.balls_field:
            self.x_pos, self.y_pos, color, ball_label = ball
            ball_label.setGeometry(ball[0], ball[1], self.ball_size, self.ball_size)
            ball_label.setMouseTracking(True)
            ball_label.setStyleSheet(f"background-color: {ball[2]}; "
                                     f"border-radius: {self.ball_size // 2}px; "
                                     f"border: 1px solid black;")
        self.row = total_rows
        self.shooter_color = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink'])
        self.shooter = QLabel(self)
        self.shooter.setGeometry(int(screen_width // 2 - self.ball_size // 2 - 10),
                                 int(screen_height - self.ball_size * 1.5), 100, 100)  # серый кружок снизу
        self.shooter.setStyleSheet(f"background-color: {self.shooter_color}; "
                                   "border-radius: 50px; "
                                   "border: 1px solid black;")  # настройка цвета и формы серого кружка
        self.score = 0
        self.score_label = QLabel('Очки: 0',self)
        self.score_label.setGeometry(0, screen_height - 100, 400, 100)
        self.score_label.setStyleSheet('background: transparent;font: 32pt "Century Schoolbook";color: rgb(0, 0, 0);')

    def paintEvent(self, event):  # пушка-дуло-пулемет
        self.shooter.setStyleSheet(f"background-color: {self.shooter_color}; "
                                   "border-radius: 50px; "
                                   "border: 1px solid black;")
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(QBrush(Qt.black))
        painter.save()
        painter.translate(self.width() // 2, self.height() - self.ball_size // 2)
        painter.rotate(1 * shooter_angle - 0)  # 90
        painter.drawRect(-100, -self.ball_size // 4, 100, self.ball_size // 2)
        painter.restore()
        if self.current_ball is not None:
            painter.setBrush(QBrush(QColor(self.current_ball[2])))
            painter.drawEllipse(int(self.current_ball[0]), int(self.current_ball[1]), int(self.ball_size),
                                int(self.ball_size))

    def mouseMoveEvent(self, event):
        # Рассчитываем угол относительно центра стрелы и курсора мыши
        global shooter_angle
        dx = event.x() - (self.width() // 2)
        dy = -1 * (event.y() - (self.height()))
        shooter_angle = -1 * (math.degrees(math.atan2(dy, dx)) - 180)
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_shooting()

    def start_shooting(self):
        if self.current_ball == None:
            self.current_ball = [self.width() // 2 - self.ball_size // 2, self.height() - self.ball_size * 1.5 + 50, self.shooter_color]
            self.shooter_color = get_random_color()
            self.shooting_angle = shooter_angle
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_shooting_ball)
            self.timer.start(1)  # время паузы между шагами (в миллисекундах)
            self.update()

    def update_shooting_ball(self):
        if self.current_ball is not None and self.can_checking:
            #self.can_checking = False
            dx = math.cos(math.radians(self.shooting_angle)) * self.shooting_power
            dy = math.sin(math.radians(self.shooting_angle)) * self.shooting_power
            self.current_ball[0] -= dx
            self.current_ball[1] -= dy

            # Проверяем столкновение с границами экрана
            if self.current_ball[0] <= 0 or self.current_ball[0] + self.ball_size >= screen_width:
                self.shooting_angle = 180 - self.shooting_angle
            if self.current_ball[1] <= 0 or self.current_ball[1] + self.ball_size >= screen_height:
                self.shooting_angle = -self.shooting_angle
            self.check_collision_new()
            self.update()
            self.can_checking = True

    def check_collision_new(self):
        min_ball = None
        min_dist = 0
        for ball in self.balls_field:
            distance = math.sqrt(
                (self.current_ball[0] - ball[0]) ** 2 + (self.current_ball[1] - ball[1]) ** 2)
            if min_ball == None or distance<min_dist:
                min_ball = ball
                min_dist = distance
        if min_dist < self.ball_size and min_ball != None:
            if self.current_ball[0] - min_ball[0] > 0:
                new_pos_x = min_ball[0]+math.cos(math.radians(60))*self.ball_size
            else:
                new_pos_x = min_ball[0]-math.cos(math.radians(60))*self.ball_size
            if self.current_ball[1] - min_ball[1] < self.ball_size / 10:
                new_pos_y = min_ball[1]
                if self.current_ball[0] - min_ball[0] > 0:
                    new_pos_x = min_ball[0]+self.ball_size
                else:
                    new_pos_x = min_ball[0]-self.ball_size
            elif self.current_ball[1] - min_ball[1] > 0:
                new_pos_y = min_ball[1]+math.sin(math.radians(60))*self.ball_size
            else:
                new_pos_y = min_ball[1]-math.sin(math.radians(60))*self.ball_size
            self.current_ball[0] = new_pos_x
            self.current_ball[1] = new_pos_y
            if (self.check_remove()):
                print('destroy!')
                self.score_label.setText('Очки: '+str(self.score))
                self.timer.stop()
                self.current_ball = None
            else:
                if new_pos_y > screen_height - 4*self.ball_size:
                    self.close()
                    self.player.stop()
                    self.endG = EndGame(self.score, 0)
                    self.endG.showMaximized()
                print('append!')
                self.attach_ball()
                self.timer.stop()
                self.current_ball = None
            self.num_step += 1
            if self.num_step%10 == 0:
                for ball in self.balls_field:
                    ball[1] += round(self.ball_size * math.sin(math.radians(60)))
                    if ball[1] > screen_width - 4*self.ball_size:
                        self.close()
                        self.player.stop()
                        self.endG = EndGame(self.score, 0)
                        self.endG.showMaximized()
                    ball[3].hide()
                    ball[3] = QLabel(self)
                    ball[3].setGeometry(ball[0], ball[1], self.ball_size, self.ball_size)
                    ball[3].setMouseTracking(True)
                    ball[3].setStyleSheet(f"background-color: {ball[2]}; "
                                     f"border-radius: {self.ball_size // 2}px; "
                                     f"border: 1px solid black;")
                    ball[3].show()
                tmp = self.num_step // 10
                if tmp%2 == 0:
                    new_x_pos = 0
                    num_ball = self.column
                else:
                    new_x_pos = self.ball_size // 2
                    num_ball = self.column - 1
                new_y_pos = 0
                for i in range(num_ball):
                    color = random.choice(['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink'])  # Randomly choose red, green, or blue
                    ball = [int(new_x_pos), int(new_y_pos), color, QLabel(self)]
                    ball[3].setGeometry(ball[0], ball[1], self.ball_size, self.ball_size)
                    ball[3].setMouseTracking(True)
                    ball[3].setStyleSheet(f"background-color: {ball[2]}; "
                                     f"border-radius: {self.ball_size // 2}px; "
                                     f"border: 1px solid black;")
                    ball[3].show()
                    self.balls_field.append(ball)
                    new_x_pos += self.ball_size
        
                
    def check_remove(self):
        mylen = 1
        balls_to_remove = []
        balls_to_remove.append(self.current_ball)
        i = 0
        while i < mylen:
            for ball in self.balls_field:
                distance = math.sqrt(
                    (balls_to_remove[i][0] - ball[0]) ** 2 + (balls_to_remove[i][1] - ball[1]) ** 2)
                if distance < self.ball_size*1.1 and ball[2] == balls_to_remove[i][2] and ball not in balls_to_remove:
                    balls_to_remove.append(ball)
                    mylen += 1
            i += 1
        balls_to_remove.remove(self.current_ball)
        if mylen > 2:
            print(balls_to_remove)
            self.score += 100+100*len(balls_to_remove)
            for ball in balls_to_remove:
                self.remove_ball(ball)
            test_balls = []
            for ball in balls_to_remove:
                for my_ball in self.balls_field:
                    if my_ball not in balls_to_remove and my_ball not in test_balls:
                        distance = math.sqrt((my_ball[0] - ball[0]) ** 2 + (my_ball[1] - ball[1]) ** 2)
                        if distance < self.ball_size*1.1:
                            test_balls.append(my_ball)
            for ball in test_balls:
                if ball in self.balls_field:
                    self.check_test_ball(ball)
            return True
        else:
            return False
                
        if len(self.balls_field) == 0:
            self.close()
            self.player.stop()
            self.endG = EndGame(self.score, 1)
            self.endG.showMaximized()
    
    def check_test_ball(self, my_ball):
        w_exit = False
        old_len = 0
        m_balls = [my_ball]
        while not w_exit and old_len != len(m_balls):
            old_len = len(m_balls)
            for i in range(old_len):
                for ball in self.balls_field:
                    if ball not in m_balls:
                        distance = math.sqrt((m_balls[i][0] - ball[0]) ** 2 + (m_balls[i][1] - ball[1]) ** 2)
                        if distance < self.ball_size*1.1:
                            m_balls.append(ball)
                            if ball[1] == 0:
                                w_exit = True
        if not w_exit:
            for ball in m_balls:
                self.remove_ball(ball)
    
    def check_collision(self):
        for ball in self.balls_field:
            distance = math.sqrt(
                (self.current_ball[0] - ball[0]) ** 2 + (self.current_ball[1] - ball[1]) ** 2)
            if round(distance) < self.ball_size:
                if self.current_ball[2] == ball[2]:
                    print(f'{self.current_ball[2]} == {ball[2]}')
                    print('destroy!')
                    self.timer.stop()
                    self.current_ball = None
                    self.remove_ball(ball)
                    break
                else:
                    if self.current_ball[0] - ball[0] > 0:
                        new_pos_x = ball[0]+math.cos(math.radians(60))*self.ball_size
                    else:
                        new_pos_x = ball[0]-math.cos(math.radians(60))*self.ball_size
                    new_pos_y = ball[1]+math.sin(math.radians(60))*self.ball_size
                    print(f'{self.current_ball[2]} != {ball[2]}')
                    print('append!')
                    self.current_ball[0] = new_pos_x;
                    self.current_ball[1] = new_pos_y;
                    self.attach_ball()
                    self.timer.stop()
                    self.current_ball = None
                    break

    def attach_ball(self):
        new_ball = [int(self.current_ball[0]), int(self.current_ball[1]), self.current_ball[2], QLabel(self)]
        self.balls_field.append(new_ball)
        new_ball[3].setGeometry(new_ball[0], new_ball[1], self.ball_size, self.ball_size)
        new_ball[3].setMouseTracking(True)
        new_ball[3].setStyleSheet(f"background-color: {self.current_ball[2]}; "
                                 f"border-radius: {self.ball_size // 2}px; "
                                 f"border: 1px solid black;")
        new_ball[3].show()
        
    def remove_ball(self, ball):
        self.balls_field.remove(ball)
        ball[3].hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            self.start_shooting()

    def setupMediaPlayer(self):
        self.player = QMediaPlayer()
        url = QUrl.fromLocalFile("TinyBubbles.mp3")
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.mediaStatusChanged.connect(self.repeatMusic)
        self.player.play()

    def repeatMusic(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.play()


class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.game_window = None

        global screen_width, screen_height
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        self.setWindowTitle("Шарики")
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0.767, y1:0, x2:0, y2:1, stop:0 rgba(0, 0, 47, 255), stop:1 rgba(21, 21, 21, 255))')

        start_button = QPushButton("Начать игру", self)
        start_button.setGeometry(screen_width // 2 - 50, screen_height // 2 + 200, 200, 100)
        start_button.clicked.connect(self.start_game)
        start_button.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.494318, y2:0.926, stop:0 rgba(0, 0, 214, 255), stop:0.897727 rgba(24, 15, 122, 255));font: 75 18pt "Century Schoolbook";border-radius : 50;color: rgb(255, 255, 255);')

        exit_button = QPushButton("Выйти", self)
        exit_button.setGeometry(0, 0, 150, 50)
        exit_button.clicked.connect(self.close)
        exit_button.setStyleSheet(
            'background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.494318, y2:0.926, stop:0 rgba(0, 0, 214, 255), stop:0.897727 rgba(24, 15, 122, 255)) ;font: 75 18pt "Century Schoolbook";border-radius : 25;color: rgb(255, 255, 255); ')

        game_name = QLabel('Шарики', self)
        game_name.setGeometry(screen_width // 2 - 200, screen_height // 2 - 400, 500, 150)
        game_name.setAlignment(Qt.AlignCenter)
        game_name.setStyleSheet('background: transparent;font: 72pt "Century Schoolbook";color: rgb(255, 255, 255);')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Space:
            self.start_game()

    def start_game(self):
        self.game_window = GameWindow()
        self.close()
        self.game_window.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    start_window = StartWindow()
    start_window.showMaximized()
    sys.exit(app.exec_())
