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
        color = line["цвет"]
        if color not in color_ids:
            create_color_query = f'INSERT INTO colors (name) VALUES ("{color}")'
            cur.execute(create_color_query)
            color_id = cur.execute(f'SELECT id FROM colors WHERE name = "{color}";').fetchall()[0][0]
            color_ids[color] = color_id
        query += f'("{line["название"]}", {color_ids[color]}, "{line["id изображения"]}"),\n'
    query = query[:-2]
    cur.execute(query)
    con.commit()
