#!../venv/bin/python
from env import *
import yaml
def create_menu(data):
    data['created_by'] = 'seed'
    data['updated_by'] = 'seed'
    am = m.EltAppMenu(**data)
    db.session.add(am)
    db.session.commit()
    return am

def deserialize(row):
    rec = row.split(';')
    code = rec[0]
    text = rec[1]
    url = None
    if len(rec) == 3: url = rec[2]
    d = { 'code': code, 'text': text, 'url': url }
    return d

def seed_menu(data, parent_id=None):
    if isinstance(data, dict):
        for k, v in data.iteritems():
            d = deserialize(k)
            d['parent_id'] = parent_id
            menu = create_menu(d)
            seed_menu(v, menu.id)

    if isinstance(data, list):
        for k in data:
            d = deserialize(k)
            d['parent_id'] = parent_id
            create_menu(d)

if __name__ == '__main__':
    with app.app_context():
        f = open('dump_menu.yml', 'r')
        ast = yaml.load(f.read())
        seed_menu(ast)
        print 'CREATE MENU COMPLETED !'
