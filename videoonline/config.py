class Config(object):
    '''Base config class'''
    CSRF_ENABLED = True
    SECRET_KEY = "9c86dedd338c33f1a5009273e212e464"
    pass

class ProdConfig(object):
    '''Production config class'''
    pass

class DevConfig(object):
    '''Development config class'''
    DEBUG = True
    # Mysql Connection
    # database_type+driver://user:password@sql_server_ip:port/database_name?charset=utf-8
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123@localhost:3306/videool'

    CSRF_ENABLED = True
    SECRET_KEY = "9c86dedd338c33f1a5009273e212e464"