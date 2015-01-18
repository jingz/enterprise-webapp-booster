#!/usr/bin/env python

import os
import sys
import commands

def get_config(app_dir):
    sys.path.append(app_dir)
    env = os.environ.get('ENLIGHTEN_ENV', 'dev')
    mod = __import__('settings', fromlist=['settings'])
    settings_name = '%sConfig' % env.capitalize()
    settings = getattr(mod, settings_name)
    return settings

def gen_code(settings, table_name):
    cmd = 'sqlacodegen --tables %s %s | ./flaskchem.py' % (table_name, settings.SQLALCHEMY_DATABASE_URI)
    return commands.getoutput(cmd)

if __name__ == '__main__':
    table_name = sys.argv[1]
    settings = get_config('..')
    print gen_code(settings, table_name)
