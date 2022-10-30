from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from sys import argv, exit


class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./windows/search.ui', self)


class AddWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./windows/add.ui', self)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./windows/main.ui', self)
        self.setupUi()

    def setupUi(self):
        self.search_window = SearchWindow()
        self.add_window = AddWindow()
        self.search_button.clicked.connect(self.open_search_window)
        self.add_button.clicked.connect(self.open_add_window)

    def open_search_window(self):
        self.search_window.show()

    def open_add_window(self):
        self.add_window.show()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())
