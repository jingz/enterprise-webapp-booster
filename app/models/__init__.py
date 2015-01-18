import os
import sys
import importlib

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()

def get_model_classes():
    path = os.path.dirname(os.path.abspath(__file__))
    klasses = []
    for py_file in [f.split('.')[0] for f in os.listdir(path) if f.endswith('.py') and f != '__init__.py']:
        mod = __import__('.'.join([__name__, py_file]), fromlist=[py_file])
        klasses.extend(
            getattr(mod, x) for x in dir(mod)
            if isinstance(getattr(mod, x), type) and
               issubclass(getattr(mod, x), db.Model)
        )
    return klasses

def init_model_classes():
    for model in get_model_classes():
        setattr(sys.modules[__name__], model.__name__, model)

init_model_classes()
