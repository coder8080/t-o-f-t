from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton
from PyQt5 import uic
from .item_window import ItemWindow


class SearchWindow(QMainWindow):
    """ Окно поиска по забытым вещам """

    def __init__(self, cur, con):
        super().__init__()
        self.cur = cur
        self.con = con
        self.colors = []
        self.db_colors_ids = dict()
        self.db_colors_names = dict()
        self.item_window = ItemWindow(self.cur, self.con, self.close)
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

    def reset_table(self):
        self.table.setRowCount(0)

    def closeEvent(self, event):
        self.reset_name()
        self.reset_color_value()
        self.reset_statusbar()
        self.reset_table()

    def onclick_fabric(self, id):
        def result():
            self.item_window.fetchData(id)
            self.item_window.show()
        return result

    def update_colors(self):
        """ Обновить список цветов """
        self.reset_colors()
        queryColors = self.cur.execute(
            'SELECT * FROM colors').fetchall()
        for id, name in queryColors:
            self.db_colors_ids[name] = id
            self.db_colors_names[id] = name
        self.colors = ['Любой'] + [el[1] for el in queryColors]
        self.color_box.addItems(self.colors)

    def search(self):
        """ Выполнить поиск """
        name = self.name_edit.text()
        color = self.color_box.currentText()
        if color == 'Любой':
            color = None
        # Формирование запроса
        query = 'SELECT  name, color_id, id FROM things'
        if name or color:
            query += ' WHERE'
            if name:
                query += f' levenshtein(name, "{name}") < 4'
            if name and color:
                query += ' AND'
            if color:
                color_id = self.db_colors_ids[color]
                query += f' color_id = {color_id}'
        query += ';'
        result = self.cur.execute(query).fetchall()
        # Отображение данных в таблице
        self.table.setRowCount(len(result))
        for i, row in enumerate(result):
            self.table.setItem(i, 0, QTableWidgetItem(row[0]))
            self.table.setItem(i, 1, QTableWidgetItem(
                self.db_colors_names[row[1]]))
            button = QPushButton('Открыть', self)
            button.clicked.connect(self.onclick_fabric(row[2]))
            self.table.setCellWidget(i, 2, button)
        if len(result) > 0:
            self.statusbar.showMessage('Успешно')
        else:
            self.statusbar.showMessage('Записи не найдены')
