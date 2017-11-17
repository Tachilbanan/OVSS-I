import os

''' GENERATE SECRET KEY '''
# 参照 CTFd 的写法
with open('.web_secret_key', 'a+b') as secret:
    secret.seek(0)  # Seek to beginning of file since a+ mode leaves you at the end and w+ deletes the file
    key = secret.read()
    if not key:
        key = os.urandom(64)
        secret.write(key)
        secret.flush()


class Config(object):
    '''Base config class'''
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or key

    CACHE_TYPE = 'simple'
    ASSETS_DEBUG = True
    # 视频上传目录
    UPLOADED_VIDEOS_DEST = 'videoonline/theme/static/videos'
    UPLOADED_IMAGES_DEST = 'videoonline/theme/static/photos'
    # Mysql Connection
    # database_type+driver://user:password@sql_server_ip:port/database_name?charset=utf-8
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/videool'


class ProdConfig(object):
    '''Production config class'''
    pass


class DevConfig(object):
    '''Development config class'''
    DEBUG = True
    CACHE_TYPE = 'simple'
    ASSETS_DEBUG = True

    # 视频上传目录
    UPLOADED_VIDEOS_DEST = 'videoonline/theme/static/videos'
    UPLOADED_IMAGES_DEST = 'videoonline/theme/static/photos'

    # Mysql Connection
    # database_type+driver://user:password@sql_server_ip:port/database_name?charset=utf-8
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/videool'

    CSRF_ENABLED = True
    SECRET_KEY = "9c86dedd338c33f1a5009273e212e464"
