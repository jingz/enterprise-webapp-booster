#!../venv/bin/python

from env import app, db, m
with app.app_context():
    admin = m.EltRole.query.filter(m.EltRole.role_name == 'admin').one()
    operator = m.EltRole.query.filter(m.EltRole.role_name == 'operator').one()
    marketing = m.EltRole.query.filter(m.EltRole.role_name == 'marketing').one()

    u = m.EltUser.query.filter(m.EltUser.username == 'admin').one()

    db.session.add(m.EltUserRole(role_id=admin.id, user_id=u.id, created_by='seed', updated_by='seed'))
    db.session.add(m.EltUserRole(role_id=operator.id, user_id=u.id, created_by='seed', updated_by='seed'))
    db.session.add(m.EltUserRole(role_id=marketing.id, user_id=u.id, created_by='seed', updated_by='seed'))
    db.session.commit()

    print "Create Role For Admin !!"
