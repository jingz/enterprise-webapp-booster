#!../venv/bin/python
import os
import sys

project_dir = os.path.abspath('../')
sys.path.append(project_dir)
from enlighten import create_app
from enlighten import db
app = create_app('enlighten.settings.DevConfig', env='dev')

from prettytable import PrettyTable
with app.app_context():
    t = PrettyTable()
    t.add_column('RULES', [r.rule for r in app.url_map.iter_rules()])
    t.add_column('METHODS', [r.methods for r in app.url_map.iter_rules()])
    t.add_column('ENDPOINT', [r.endpoint for r in app.url_map.iter_rules()])
    t[0].align = 'l'
    print t
