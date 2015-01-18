#! ../env/bin/python
import os

from flask import Flask
from webassets.loaders import PythonLoader as PythonAssetsLoader

from app import assets
from app.models import db
# from app.sessions import DBSessionInterface
from flask_kvsession import KVSessionExtension
from simplekv.db.sql import SQLAlchemyStore
from .extensions import CustomJSONEncoder

from app.extensions import (
    cache,
    assets_env,
    debug_toolbar,
    login_manager,
    kv_session,
    #principal,
)


def create_app(object_name, env="prod"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. app.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    __app = Flask(__name__)

    __app.config.from_object(object_name)
    __app.config['ENV'] = env
    __app.json_encoder = CustomJSONEncoder

    #init the cache
    cache.init_app(__app)

    debug_toolbar.init_app(__app)

    #init SQLAlchemy
    db.init_app(__app)

    login_manager.init_app(__app)

    # Import and register the different asset bundles
    assets_env.init_app(__app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in assets_loader.load_bundles().iteritems():
        assets_env.register(name, bundle)

    # register our blueprints
    # from controllers.main import main
    # app.register_blueprint(main)

    # from controllers.client_controller import bp as client_blueprint
    # app.register_blueprint(client_blueprint, url_prefix='/clients')

    # use when require user-permission system
    # from controllers.main import main
    # __app.register_blueprint(main)

    from controllers.admin_controller import bp as admin_blueprint
    __app.register_blueprint(admin_blueprint, url_prefix='/')

    from controllers.feed_controller import bp as feed_blueprint
    __app.register_blueprint(feed_blueprint, url_prefix='/feeds')

    from controllers.entries_controller import bp as entries_blueprint
    __app.register_blueprint(entries_blueprint, url_prefix='/feed_entries')

    # from controllers.inq_controller import bp as inq_blueprint
    # __app.register_blueprint(inq_blueprint, url_prefix='/inq')


    # app.session_interface = DBSessionInterface()

    # init principal
    # principal.init_app(app)

    # @__app.before_first_request
    # def setup_session_db(*args, **kwds):
    #     session_store = SQLAlchemyStore(db.engine, db.metadata, 'elt_session')
    #     kv_session.init_app(__app, session_store)

    return __app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    __app = create_app('app.settings.%sConfig' % env.capitalize(), env=env)

    __app.run()
