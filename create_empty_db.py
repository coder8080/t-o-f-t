import sqlite3


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_column = range(n+1)
    for i in range(1, m+1):
        previous_column, current_column = current_column, [i]+[0]*n
        for j in range(1, n+1):
            add, delete, change = previous_column[j] + \
                1, current_column[j-1]+1, previous_column[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_column[j] = min(add, delete, change)

    return current_column[n]


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
con.create_function('levenstein', 2, distance)
con.commit()
con.close()
print('Успешно')
