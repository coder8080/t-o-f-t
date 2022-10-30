from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox
from PyQt5 import uic
from sys import argv, exit
import sqlite3

DATABASE_FILENAME = './database.sqlite3'


class SearchWindow(QMainWindow):
    def __init__(self, cur, con):
        super().__init__()
        self.cur = cur
        self.con = con
        self.initUi()

    def initUi(self):
        uic.loadUi('./windows/search.ui', self)
        self.cancel_button.clicked.connect(self.reset_and_close)

    def reset_and_close(self):
        self.close()


class AddWindow(QMainWindow):
    def __init__(self, cur, con):
        super().__init__()
        self.cur = cur
        self.con = con
        self.colors = []
        self.filename = ''
        self.initUi()
        self.update_colors()

    def initUi(self):
        uic.loadUi('./windows/add.ui', self)
        self.cancel_button.clicked.connect(self.close)
        self.add_color_button.clicked.connect(self.add_color)
        self.image_button.clicked.connect(self.open_image)

    def reset(self):
        self.filename = 'Файл не выбран'
        self.update_filename()

    def closeEvent(self, e):
        self.reset()
        self.close()

    def add_color(self):
        colorname = QInputDialog.getText(
            self, "Добавление цвета", "Название цвета")[0].lower()
        if not colorname:
            return
        isExisting = bool(self.cur.execute(
            f'SELECT * FROM colors WHERE name = "{colorname}"').fetchall())

        if isExisting:
            QMessageBox().warning(self, 'Добавление цвета', 'Такой цвет уже существует',
                                  QMessageBox.StandardButton.Ok)
        else:
            self.cur.execute(f'INSERT INTO colors (name) VALUES'
                             f' ("{colorname}")')
            self.con.commit()
            QMessageBox().information(self, 'Добавление цвета', 'Цвет успешно добавлен',
                                      QMessageBox.StandardButton.Ok)
            self.update_colors()
            self.color_box.setCurrentIndex(self.colors.index(colorname))

    def update_colors(self):
        self.color_box.clear()
        dbColors = self.cur.execute(f'SELECT name FROM colors').fetchall()
        self.colors = [el[0] for el in dbColors]
        self.color_box.addItems(self.colors)

    def update_filename(self):
        self.image_path.setText(self.filename)

    def open_image(self):
        filename = QFileDialog.getOpenFileName(
            self, 'Выберите файл с изображением', '',
            'Image Files(*.jpg, *.jpeg, *.png, *.bpm, *.webp)')[0]
        if not filename:
            QMessageBox().warning(self, 'Ошибка', 'Файл не был выбран. Скорее'
                                  ' всего, вы нажали "Cancel" вместо "Open"')
            return
        self.filename = filename
        self.update_filename()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./windows/main.ui', self)
        self.setupDb()
        self.setupUi()

    def setupUi(self):
        self.search_window = SearchWindow(self.cur, self.con)
        self.add_window = AddWindow(self.cur, self.con)
        self.search_button.clicked.connect(self.open_search_window)
        self.add_button.clicked.connect(self.open_add_window)

    def setupDb(self):
        self.con = sqlite3.connect(DATABASE_FILENAME)
        self.cur = self.con.cursor()

    def open_search_window(self):
        self.search_window.show()

    def open_add_window(self):
        self.add_window.show()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())
