import random
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        row = 5
        column = 11
        balls_field = []

        for i in range(row):
            row_list = []
            for j in range(column):
                cell = random.randint(1, 3)
                row_list.append(cell)
            balls_field.append(row_list)

        self.setWindowTitle("Bubble Shooter")
        self.setGeometry(100, 100, 400, 300)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(50, 50, 300, 200)
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(column)

        for i in range(row):
            for j in range(column):
                item = QTableWidgetItem()
                item.setText(str(balls_field[i][j]))
                self.tableWidget.setItem(i, j, item)

        self.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
