#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from flask.ext.migrate import Migrate, MigrateCommand

from app import create_app
from app.models import db

# default to dev config because no one should use this in
env = 'dev'
__app = create_app('app.settings.%sConfig' % env.capitalize(), env=env)

manager = Manager(__app)
migrate = Migrate(__app, db)

manager.add_command("server", Server())
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    import app.models
    from pprint import pprint
    return dict(app=__app, db=db, m=app.models, pp=pprint)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """

    db.create_all()

from prettytable import PrettyTable
import re
@manager.command
def routes():
    ignore = re.compile('_debug_toolbar')
    with __app.app_context():
        t = PrettyTable()
        ir = __app.url_map.iter_rules
        #t.add_column('#', [i for i, r in enumerate(iter_routes) if not ignore.search(r.rule)])
        t.add_column('RULES', [r.rule for r in ir() if not ignore.search(r.rule)])
        t.add_column('METHODS', [r.methods for r in ir() if not ignore.search(r.rule)])
        t.add_column('ENDPOINT', [r.endpoint for r in ir() if not ignore.search(r.rule)])
        t[0].align = 'l'
        print t

@manager.command
def fetch():
    with __app.app_context():
        from tasks.fetching_feeds import run
        run()

@manager.command
def today():
    with __app.app_context():
        from tasks.pop import run
        run()

if __name__ == "__main__":
    manager.run()
