from sqlite3 import OperationalError
import sys

# Глобальные константы
if hasattr(sys, "_MEIPASS"):
    ROOT = './'
else:
    ROOT = '../../'
DATABASE_FILENAME = './database.sqlite3'
LOADING_ERROR = (OperationalError, IndexError)
FILE_GENERATED = 'Файл сгенерирован'
LOADING_ERROR_MESSAGE = 'Ошибка при загрузке данных'
UNKNOWN_ERROR_MESSAGE = 'Ошибка'
