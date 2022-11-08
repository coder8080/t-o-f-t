from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from .search_window import SearchWindow
from .add_window import AddWindow
from .files_window import FilesWindow
from .helpers.database import create_database, distance
from .helpers.constants import *
from .helpers.logger_instance import logger
from os import path
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./windows/main.ui', self)
        self.setupDb()
        self.initUi()

    def initUi(self):
        self.search_window = SearchWindow(self.cur, self.con)
        self.add_window = AddWindow(self.cur, self.con)
        self.files_window = FilesWindow(self.cur, self.con)

        self.search_button.clicked.connect(self.open_search_window)
        self.add_button.clicked.connect(self.open_add_window)
        self.file_button.clicked.connect(self.open_files_window)

    def setupDb(self):
        """ Установить соединение с базой данных """
        if not path.exists(DATABASE_FILENAME):
            create_database()
        self.con = sqlite3.connect(DATABASE_FILENAME)
        self.con.create_function('levenshtein', 2, distance)
        self.cur = self.con.cursor()

    def open_search_window(self):
        self.search_window.update_colors()
        self.search_window.show()

    def open_add_window(self):
        self.add_window.show()

    def open_files_window(self):
        self.files_window.show()

    def closeEvent(self, event):
        logger.close()
