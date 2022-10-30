import sqlite3

print('Создаю файл')
file = open('database.sqlite3', mode='wb')
file.close()
del file

print('Файл создан')
print('Подключаюсь')
con = sqlite3.connect('database.sqlite3')
cur = con.cursor()

print('Создаю таблицу цветов')
cur.execute('CREATE TABLE colors (id primary key, name text);')
print('Создаю таблицу потерянных вещей')
cur.execute('CREATE TABLE things (id primary key, name text,'
            ' color_id integer, image_filename text)')
print('Добавляю основные цвета')
cur.execute('INSERT INTO colors (name) VALUES ("красный"),'
            ' ("синий"), ("зелёный"), ("белый"), ("чёрный")')
print('Успешно')
