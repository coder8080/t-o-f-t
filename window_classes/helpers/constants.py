from sqlite3 import OperationalError

# Глобальные константы
DATABASE_FILENAME = './database.sqlite3'
LOADING_ERROR = (OperationalError, IndexError)
FILE_GENERATED = 'Файл сгенерирован'
LOADING_ERROR_MESSAGE = 'Ошибка при загрузке данных'
UNKNOWN_ERROR_MESSAGE = 'Ошибка'
