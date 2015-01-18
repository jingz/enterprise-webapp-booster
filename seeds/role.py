#!../venv/bin/python

from env import app, db, m
with app.app_context():
    admin = m.EltRole(role_name='admin', 
                  role_desc='system adminstator',
                  updated_by='seed',
                  created_by='seed')

    operator = m.EltRole(role_name='operator', 
                  role_desc='system operator',
                  updated_by='seed',
                  created_by='seed')

    marketing = m.EltRole(role_name='marketing', 
                  role_desc='system marketing',
                  updated_by='seed',
                  created_by='seed')

    db.session.add(admin)
    db.session.add(operator)
    db.session.add(marketing)
    db.session.commit()

    print "Create Role; Admin, Operator, Marketing"
       
