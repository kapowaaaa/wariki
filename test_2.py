import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QGridLayout
from PyQt5.QtGui import QPixmap


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        rows = 5
        columns = 11

        ball_images = ["ball1.png", "ball2.png", "ball3.png"]  # Замените на фактические имена файлов изображений шариков

        layout = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        for i in range(rows):
            for j in range(columns):
                ball_label = QLabel()
                ball_index = random.randint(0, 2)  # Генерация случайного индекса изображения шарика
                pixmap = QPixmap(ball_images[ball_index])
                scaled_pixmap = pixmap.scaled(50, 50)  # Установка размера 50x50 для изображения шарика
                ball_label.setPixmap(scaled_pixmap)
                layout.addWidget(ball_label, i, j)

        self.setWindowTitle("Bubble Shooter")
        self.setGeometry(0, 0, 1920, 1080)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
