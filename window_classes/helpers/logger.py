from datetime import datetime
import csv


class Logger:
    """ Инструмент сохранения записей о событиях """

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'w', newline='', encoding="utf8")
        self.writer = csv.DictWriter(
            self.file, fieldnames=['время', 'имя', 'название', 'цвет'], delimiter=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        self.writer.writeheader()

    def log(self, name, thing, color):
        now = str(datetime.now())
        self.writer.writerow(
            {'время': now, 'имя': name, 'название': thing, 'цвет': color})

    def close(self):
        self.file.close()
