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
cur.execute(
    'CREATE TABLE colors (id INTEGER PRIMARY KEY AUTOINCREMENT, name text);').fetchall()
print('Создаю таблицу потерянных вещей')
cur.execute('CREATE TABLE things (id INTEGER PRIMARY KEY AUTOINCREMENT, name text,'
            ' color_id integer, filename_id text)').fetchall()
print('Добавляю основные цвета')
cur.execute('INSERT INTO colors (name) VALUES ("красный"),'
            ' ("синий"), ("зелёный"), ("белый"), ("чёрный")').fetchall()
con.commit()
con.close()
print('Успешно')
