from email.charset import QP
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QMessageBox, QTableWidgetItem, QPushButton
from PyQt5 import uic
from sys import argv, exit
from PIL import Image
import os
import sqlite3
import uuid0

DATABASE_FILENAME = './database.sqlite3'


def create_database():
    file = open(DATABASE_FILENAME, mode='wb')
    file.close()
    del file
    con = sqlite3.connect('database.sqlite3')
    cur = con.cursor()
    cur.execute(
        'CREATE TABLE colors (id INTEGER PRIMARY KEY AUTOINCREMENT, name text);').fetchall()
    cur.execute('CREATE TABLE things (id INTEGER PRIMARY KEY AUTOINCREMENT, name text,'
                ' color_id integer, filename_id text)').fetchall()
    cur.execute('INSERT INTO colors (name) VALUES ("красный"),'
                ' ("синий"), ("зелёный"), ("белый"), ("чёрный")').fetchall()
    con.commit()
    con.close()


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_column = range(n+1)
    for i in range(1, m+1):
        previous_column, current_column = current_column, [i]+[0]*n
        for j in range(1, n+1):
            add, delete, change = previous_column[j] + \
                1, current_column[j-1]+1, previous_column[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_column[j] = min(add, delete, change)

    return current_column[n]


def save_image(filename, id):
    if not os.path.exists('./images'):
        os.mkdir('./images')
    im = Image.open(filename)
    copy_filename = f'./images/{id}.png'
    im.save(copy_filename)


class SearchWindow(QMainWindow):
    def __init__(self, cur, con):
        super().__init__()
        self.cur = cur
        self.con = con
        self.colors = []
        self.db_colors_ids = dict()
        self.db_colors_names = dict()
        self.initUi()
        self.update_colors()

    def initUi(self):
        uic.loadUi('./windows/search.ui', self)
        self.cancel_button.clicked.connect(self.close)
        self.search_button.clicked.connect(self.search)
        self.init_table()
        self.reset_statusbar()

    def init_table(self):
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(('Название', 'Цвет', 'Просмотр'))

    def reset_name(self):
        self.name_edit.setText('')

    def reset_color_value(self):
        self.color_box.setCurrentIndex(0)

    def reset_statusbar(self):
        self.statusbar.showMessage('Ожидание действий')

    def reset_colors(self):
        self.color_box.clear()
        self.colors = []
        self.db_colors_ids = dict()

    def closeEvent(self, event):
        self.reset_name()
        self.reset_color_value()
        self.reset_statusbar()

    def update_colors(self):
        self.reset_colors()
        queryColors = self.cur.execute(
            'SELECT * FROM colors').fetchall()
        for id, name in queryColors:
            self.db_colors_ids[name] = id
            self.db_colors_names[id] = name
        self.colors = ['Любой'] + [el[1] for el in queryColors]
        self.color_box.addItems(self.colors)

    def search(self):
        name = self.name_edit.text()
        color = self.color_box.currentText()
        if color == 'Любой':
            color = None
        query = 'SELECT  name, color_id FROM things'
        if name or color:
            query += ' WHERE'
            if name:
                query += f' levenshtein(name, "{name}") < 6'
            if name and color:
                query += ' AND'
            if color:
                color_id = self.db_colors_ids[color]
                query += f' color_id = {color_id}'
        query += ';'
        result = self.cur.execute(query).fetchall()
        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            self.table.setItem(i, 0, QTableWidgetItem(row[0]))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.db_colors_names[row[1]]))
            self.table.setCellWidget(i, 2,
                                     QPushButton('Открыть', self))
        if len(result) > 0:
            self.statusbar.showMessage('Успешно')
        else:
            self.statusbar.showMessage('Записи не найдены')


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
        self.submit_button.clicked.connect(self.submit)

    def reset(self):
        self.filename = 'Файл не выбран'
        self.update_filename()
        self.filename = None

    def closeEvent(self, e):
        self.reset()

    def add_color(self):
        colorname = QInputDialog.getText(
            self, "Добавление цвета", "Название цвета")[0].lower()
        if not colorname:
            return
        exists = bool(self.cur.execute(
            f'SELECT * FROM colors WHERE name = "{colorname}"').fetchall())

        if exists:
            QMessageBox().warning(self, 'Добавление цвета', 'Такой цвет уже существует',
                                  QMessageBox.StandardButton.Ok)
        else:
            self.cur.execute(f'INSERT INTO colors (name) VALUES'
                             f' ("{colorname}")')
            self.con.commit()
            QMessageBox.information(self, 'Добавление цвета', 'Цвет успешно добавлен',
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
            QMessageBox.warning(self, 'Ошибка', 'Файл не был выбран. Скорее'
                                ' всего, вы нажали "Cancel" вместо "Open"')
            return
        self.filename = filename
        self.update_filename()

    def submit(self):
        name = self.name_edit.text().lower()
        filename = self.filename
        color = self.color_box.currentText()
        if not name:
            QMessageBox.critical(
                self, 'Ошибка', 'Укажите название')
            return
        if not filename:
            QMessageBox.critical(
                self, 'Ошибка', 'Укажте имя файла с изображением')
            return
        if not color:
            QMessageBox.critical(self, 'Ошибка', 'Укажите цвет')
            return
        try:
            exists = self.cur.execute(
                f'SELECT id FROM things WHERE name = "{name}";').fetchall()
            if exists:
                QMessageBox.warning(
                    self, 'Не удалось добавить', 'Запись с таким названием уже существует',)
                return
            id = uuid0.generate()
            color_id = self.cur.execute(
                f'SELECT Id FROM colors WHERE name = "{color}"').fetchall()[0][0]
            query = f'INSERT INTO things(name, color_id, filename_id) VALUES ("{name}", {color_id}, "{id}")'
            self.cur.execute(query)
            self.con.commit()
            save_image(filename, id)
            QMessageBox.information(self, 'Уведомление', 'Запись добавлена')
            self.close()
        except (IndexError, sqlite3.OperationalError) as error:
            print(error)
            QMessageBox.critical(self, 'Произошла ошибка при обращении к базе данных.'
                                 ' Проверьте целостность файла и перезапустите приложение')
        except Exception as error:
            print(error)
            QMessageBox.critical(self, 'Произошла неизвестная ошибка. Попробуйте'
                                 ' перезапустить приложение')


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
        if not os.path.exists(DATABASE_FILENAME):
            create_database()
        self.con = sqlite3.connect(DATABASE_FILENAME)
        self.con.create_function('levenshtein', 2, distance)
        self.cur = self.con.cursor()

    def open_search_window(self):
        self.search_window.update_colors()
        self.search_window.show()

    def open_add_window(self):
        self.add_window.show()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())
