from PyQt5.QtWidgets import QFileDialog


def get_filename(instance, resolution, type):
    """ Получить имя файла в корректный форме """
    dialog_type = None
    dialog_title = None
    if type == 'save':
        dialog_type = QFileDialog.getSaveFileName
        dialog_title = 'Получившийся файл'
    elif type == 'open':
        dialog_type = QFileDialog.getOpenFileName
        dialog_title = 'Файл с данными'
    filename = dialog_type(
        instance, dialog_title, filter=f'{resolution}(*.{resolution})')[0]
    if not filename:
        return
    splitted = filename.split('.')
    if splitted[-1] != resolution:
        if filename[-1] != '.':
            filename += '.'
        filename += resolution
    return filename
