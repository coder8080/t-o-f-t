from PyQt5.QtWidgets import QMainWindow, QInputDialog
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from .helpers.constants import *
from .helpers.error_handlers import *
from .helpers.get_filename_by_id import *
from .helpers.print_document import *
from .helpers.logger_instance import logger
import os


class ItemWindow(QMainWindow):
    """ Окно с подробной информацией о предмете """

    def __init__(self, cur, con, close_search):
        super().__init__()
        self.cur = cur
        self.con = con
        self.id = 0
        self.data = dict()
        self.filename = ''
        self.close_search = close_search
        self.initUi()

    def initUi(self):
        uic.loadUi('./windows/item.ui', self)
        self.cancel_button.clicked.connect(self.close)
        self.take_button.clicked.connect(self.take)

    def fetchData(self, id):
        """ Обновить данные """
        try:
            self.data = dict()
            result = self.cur.execute(
                f'SELECT name, filename_id, color_id FROM things WHERE id={id}').fetchall()[0]
            self.data['name'] = result[0]
            self.data['filename_id'] = result[1]
            self.data['color_id'] = result[2]
            self.data['color_name'] = self.cur.execute(
                f'SELECT name FROM colors WHERE id = {self.data["color_id"]}').fetchall()[0][0]
            self.id = id
            self.updateUi()
        except LOADING_ERROR as error:
            handle_loading_error(self, error)
            self.close()
        except Exception as error:
            handle_unknown_error(self, error)
            self.close()

    def updateUi(self):
        """ Обновить интерфейс """
        self.name_label.setText(self.data['name'])
        self.color_label.setText(self.data['color_name'])
        self.filename = get_filename_by_id(self.data['filename_id'])
        pixmap = QPixmap(self.filename)
        self.image_label.setPixmap(pixmap)

    def take(self):
        """Оформить возврат """
        name = QInputDialog.getText(
            self, 'Данные', 'Введите ваше имя')[0].strip().strip('\n')
        if not name:
            QMessageBox.critical(
                self, 'Ошибка', 'Ваши персональные данные необходимы для оформления')
            return
        try:
            # Удалить запись
            self.cur.execute(f'DELETE FROM things WHERE id = {self.id}')
            self.con.commit()
            # Создать запись в логе
            logger.log(name, self.data['name'],
                       self.data['color_name'],)
            # Напечатать документ о возврате
            print_document(
                'doc.docx', name, self.data['name'], self.data['color_name'],  self.filename)
            # Удалить ненужный файл
            os.remove(self.filename)
            # Уведомить пользователя об успехе
            QMessageBox.information(self, 'Уведомление', 'Документ сохранён в'
                                    ' файл doc.docx. Обратитесь с ним в комнату'
                                    ' забытых вещей.')
            self.close_search()
            self.close()
        except LOADING_ERROR as error:
            handle_loading_error(self, error)
            return
        except Exception as error:
            handle_unknown_error(self, error)
            return
