from .constants import *

def get_filename_by_id(id: str):
    """ Возвращает имя файла по id """
    return ROOT + f'images/{id}.png'
