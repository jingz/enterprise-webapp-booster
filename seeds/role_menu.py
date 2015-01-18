#!../venv/bin/python

from env import app, db, m
with app.app_context():
    role_admin = m.EltRole.query.filter(m.EltRole.role_name == 'admin').one()

    all_menus = m.EltAppMenu.query.all()
    for menu in all_menus:
        db.session.add(m.EltRoleMenu(role=role_admin, menu=menu, created_by='seed', updated_by='seed'))

    db.session.commit()

    print "Allow admin to access to all menus !!!"
