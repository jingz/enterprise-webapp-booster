import json
from pprint import pformat
from collections import OrderedDict
from app.models import db, declared_attr

class IDMixin(object):
    id = db.Column(db.Integer, primary_key=True)

class UserstampMixin(object):
    @declared_attr
    def created_by(cls):
        return db.Column(db.String(20), nullable=False)

    @declared_attr
    def updated_by(cls):
        return db.Column(db.String(20), nullable=False)

class TimestampMixin(object):
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, nullable=False, default=db.func.now())

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())


from prettytable import PrettyTable
class AwesomeSqla(object):
    @classmethod
    def ap(cls):
        ''' docs : https://code.google.com/p/prettytable/wiki/Tutorial
            like awesome print
            show readable format of the model in console
        '''
        t = PrettyTable()
        t.add_column('Columns', [c.name for c in cls.__mapper__.c])
        t.add_column('Type', [c.type for c in cls.__mapper__.c])
        # t.add_column('Default', [c.default for c in cls.__mapper__.c])
        t[0].align = 'l'
        print t.get_string(sortby='Columns')


from searchable_mixin import SearchableMixin
class BaseMixin(AwesomeSqla, SearchableMixin, IDMixin):

    def to_dict(self):
        cls = self.__class__
        # { field: value, ... }
        d = dict([ (c.name, getattr(self, c.name)) for c in cls.__mapper__.c ])
        return d


    def update_all(self, d):
        # use searchable sanitize method
        sd = self.__class__.sanitize(d)
        for k, v in sd.iteritems():
            setattr(self, k, v)
        return sd


    def __repr__(self):
        t = PrettyTable()
        d = self.to_dict()
        return pformat(d)

