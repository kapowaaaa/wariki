import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        rows = 5
        columns = 11

        ball_images = ["ball1.png", "ball2.png", "ball3.png"]  # Замените на фактические имена файлов изображений шариков

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vertical_layout = QHBoxLayout()  # Создание вертикального макета

        for i in range(rows):
            horizontal_layout = QHBoxLayout()  # Создание горизонтального макета для каждой строки
            for j in range(columns):
                ball_label = QLabel()
                ball_index = random.randint(0, 2)  # Генерация случайного индекса изображения шарика
                pixmap = QPixmap(ball_images[ball_index])
                pixmap = pixmap.scaled(20, 20)  # Изменение размера изображения на 200x200 пикселей
                ball_label.setPixmap(pixmap)
                horizontal_layout.addWidget(ball_label)

            vertical_layout.addLayout(horizontal_layout)  # Добавление горизонтального макета в вертикальный макет

        central_widget.setLayout(vertical_layout)

        self.setWindowTitle("Bube Shooter")
        self.setGeometry(0, 0, 500, 500)
        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
