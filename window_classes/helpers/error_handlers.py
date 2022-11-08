from PyQt5.QtWidgets import QMainWindow, QMessageBox


def handle_loading_error(instance: QMainWindow, error: Exception):
    """ Выводит сообщение об ошибке загрузки """
    print(error)
    QMessageBox.critical(instance, 'Ошибка', 'Не удалось загрузить данные')


def handle_unknown_error(instance, error):
    """ Выводит сообщение о неизвестной ошибке """
    print(error)
    QMessageBox.critical(instance, 'Неизвестная ошибка',
                         'Произошла неизвестная ошибка')
