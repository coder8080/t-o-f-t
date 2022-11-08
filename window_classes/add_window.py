from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMessageBox, QFileDialog
from PyQt5 import uic
from .helpers.save_image import save_image
from .helpers.constants import *
from .helpers.error_handlers import *
import uuid0


class AddWindow(QMainWindow):
    """ Окно занесения нового предмета в базу """

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
        """ Сброс интерфейса """
        self.filename = 'Файл не выбран'
        self.update_filename()
        self.filename = None
        self.name_edit.setText('')
        self.color_box.setCurrentIndex(0)

    def closeEvent(self, e):
        self.reset()

    def add_color(self):
        """ Процесс добавления нового цвета """
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
        """ Обновить список цветов в dropdown (combo box) """
        self.color_box.clear()
        dbColors = self.cur.execute(f'SELECT name FROM colors').fetchall()
        self.colors = [el[0] for el in dbColors]
        self.color_box.addItems(self.colors)

    def update_filename(self):
        self.image_path.setText(self.filename)

    def open_image(self):
        """ Выбрать путь до файла с изображением """
        filename = QFileDialog.getOpenFileName(
            self, 'Выберите файл с изображением', '',
            'Image Files(*.jpg , *.jpeg , *.png , *.bpm , *.webp)')[0]
        if not filename:
            QMessageBox.warning(self, 'Ошибка', 'Файл не был выбран. Скорее'
                                ' всего, вы нажали "Cancel" вместо "Open"')
            return
        self.filename = filename
        self.update_filename()

    def submit(self):
        """ Создать запись """
        name = self.name_edit.text().lower()
        filename = self.filename
        color = self.color_box.currentText()
        # Валидация полей
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
            # Если запись с таким названием уже существует, то не создавать заново
            exists = self.cur.execute(
                f'SELECT id FROM things WHERE name = "{name}";').fetchall()
            if exists:
                QMessageBox.warning(
                    self, 'Не удалось добавить', 'Запись с таким названием уже существует',)
                return
            # Создание записи
            id = uuid0.generate()
            color_id = self.cur.execute(
                f'SELECT Id FROM colors WHERE name = "{color}"').fetchall()[0][0]
            query = f'INSERT INTO things(name, color_id, filename_id) VALUES ("{name}", {color_id}, "{id}")'
            self.cur.execute(query)
            self.con.commit()
            save_image(filename, id)
            QMessageBox.information(self, 'Уведомление', 'Запись добавлена')
            self.close()
        except LOADING_ERROR as error:
            handle_loading_error(self, error)
        except Exception as error:
            handle_unknown_error(self, error)
