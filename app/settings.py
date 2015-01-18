class Config(object):
    SECRET_KEY = '\xfag\xa1\x02^\x8ap\x07E\x96\xb9\x8dm4L\x13|d\xf6\xf1\x93\xdb\x91\xf3'
    # SESSION_COOKIE_NAME = 'session'
    SESSION_COOKIE_SECURE = True # only works for https environment
    # flask-login config
    SESSION_PROTECTION = 'strong'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database.db'
    CACHE_TYPE = 'simple'


class DevConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # ABOSS_DATABASE_URI = 'postgresql://aboss:password@10.4.100.144:5432/aboss_db_99'
    ABOSS_DATABASE_URI = 'postgresql://aboss:password@localhost:5432/aboss'

    dbconfig = {
        'adapter': 'postgresql',
        'user': 'jing',
        'password': '',
        'host': 'localhost',
        'port': '5432',
        'dbname': 'goodnews'
    }

    uri_pattern = '%(adapter)s://%(user)s:%(password)s@%(host)s:%(port)s/%(dbname)s'
    SQLALCHEMY_DATABASE_URI = (uri_pattern % dbconfig)
    SQLALCHEMY_ECHO = False

    # CACHE_TYPE = ''

    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False
