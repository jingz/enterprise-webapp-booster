#!../venv/bin/python

from env import app, db, m
from prettytable import PrettyTable
import re
with app.app_context():
    ignore = re.compile('_debug_toolbar|static')
    with app.app_context():
        # t = PrettyTable()
        ir = app.url_map.iter_rules
        # #t.add_column('#', [i for i, r in enumerate(iter_routes) if not ignore.search(r.rule)])
        # t.add_column('RULES', [r.rule for r in ir() if not ignore.search(r.rule)])
        # t.add_column('METHODS', [r.methods for r in ir() if not ignore.search(r.rule)])
        # t.add_column('ENDPOINT', [r.endpoint for r in ir() if not ignore.search(r.rule)])
        # t[0].align = 'l'
        # print t
        for r in ir():
            if ignore.search(r.rule): continue
            for method in r.methods:
                if method in ['OPTIONS', 'HEAD']: continue

                print 'adding', method, r.rule
                perm = m.EltApiPermission(api_name=r.endpoint, 
                        method=method,
                        created_by='seed',
                        updated_by='seed')

                db.session.add(perm)
        db.session.commit()

    # db.session.add(operator)
    # db.session.add(marketing)

    print "all permmissions are initialized"
       
