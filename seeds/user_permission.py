#!../venv/bin/python

from env import app, db, m
with app.app_context():
    perms = m.EltApiPermission.query.all()
    admin = m.EltUser.query.filter_by(username='admin').one()
    for perm in perms:
        print 'adding ', perm.api_name, perm.method, ' to session.'
        db.session.add(m.EltUserPermission(permission_id=perm.id, user_id=admin.id, 
            created_by='seed', updated_by='seed'))

    db.session.commit()
    print "Allow admin to access to all api permission !!!"
