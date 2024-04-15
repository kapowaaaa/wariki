import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class BackgroundMusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupMediaPlayer()

    def initUI(self):
        self.setWindowTitle("Continuous Background Music Player")
        self.setGeometry(300, 300, 300, 200)

    def setupMediaPlayer(self):
        # Инициализация медиаплеера
        self.player = QMediaPlayer()

        # Загрузка файла: укажите правильный путь к файлу
        url = QUrl.fromLocalFile("TinyBubbles.mp3")
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BackgroundMusicPlayer()
    ex.show()
    sys.exit(app.exec_())
