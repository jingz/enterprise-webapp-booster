from flask.ext.cache import Cache
from flask.ext.debugtoolbar import DebugToolbarExtension
from flask.ext.login import LoginManager, current_user
#from flask.ext.principal import Principal, identity_loaded, UserNeed
from flask_assets import Environment
from flask_kvsession import KVSessionExtension
from simplekv.db.sql import SQLAlchemyStore

from app.models import User

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()

debug_toolbar = DebugToolbarExtension()

# init login manager
login_manager = LoginManager()
login_manager.login_view = "main.login"

# init KV Session
kv_session = KVSessionExtension()

# CustomJSONEncoder ------------------------
from flask.json import JSONEncoder
import calendar
from datetime import datetime
from datetime import date
from decimal import Decimal

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                if obj.utcoffset() is not None:
                    obj = obj - obj.utcoffset()
                d, t = obj.isoformat().split('T')
                t = t.split('.')[0]
                return "%s %s" % (d, t)
            if isinstance(obj, date):
                return str(obj.isoformat())
            if isinstance(obj, Decimal):
                return str(obj)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)

        return JSONEncoder.default(self, obj)

