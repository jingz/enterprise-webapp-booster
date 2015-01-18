#!../venv/bin/python
# from . import app, db, m # app and models
from env import app, db, m
with app.app_context():
    u = m.EltUser(username='admin', 
                  first_name='admin',
                  password='q1W@e3r4',
                  last_name='admin',
                  email='admin@email.com', 
                  updated_by='seed',
                  created_by='seed',
                  status='A')

    db.session.add(u)
    db.session.commit()
       
