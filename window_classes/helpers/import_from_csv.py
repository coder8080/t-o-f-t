import csv


def import_from_csv(con, cur, filename):
    file = open(filename, mode='rt', encoding='utf-8')
    reader = csv.DictReader(file, delimiter=';')
    colors = cur.execute('SELECT id, name FROM colors')
    color_ids = dict()
    for id, name in colors:
        color_ids[name] = id
    query = 'INSERT INTO things (name, color_id, filename_id) VALUES '
    for line in reader:
        print(line)
        query += f'("{line["название"]}", {color_ids[line["цвет"]]}, "{line["изображение"]}"),\n'
    query = query[:-2]
    print(query)
    cur.execute(query)
    con.commit()
