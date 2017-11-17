from flask_sqlalchemy import SQLAlchemy
from videoonline.extensions import bcrypt
from flask_login import AnonymousUserMixin
import time

db = SQLAlchemy()

# 用户
class User(db.Model):
    '''Represents Proected users.'''
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, password):
        # self.id = id
        self.username = username
        self.password = self.set_password(password)

        # Setup the default-role for user.
        helper = Role.query.filter_by(name='helper').one()
        self.role = helper

    def __repr__(self):
        '''Define the string format for instance of User.'''
        return "<Model User '{}'>".format(self.username)

    def set_password(self, password):
        """Convert the password to cryptograph via flask-bcrypt"""
        return bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # 从这里往下4个方法是 Flask-Login 类处理繁琐的用户登录所需要实现的类
    def is_authenticated(self):
        """Check the user whether logged in."""
        #  检验 User 的实例化对象是否登录了.

        # Check the User's instance whether Class AnonymousUserMixin's instance.
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    # 检验用户是否通过某些验证
    def is_active():
        """Check the user whether pass the activation process."""

        return True

    # 检验用户是否为匿名用户
    def is_anonymous(self):
        """Check the user's login status whether is anonymous."""

        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    # 返回 User 实例化对象的唯一标识 id
    def get_id(self):
        """Get the user's uuid from database."""

        return str(self.id).encode()


# 权限
class Role(db.Model):
    """Represents Proected roles."""
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    users = db.relationship('User', backref='role')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)


# 视频
class Video(db.Model):
    '''Represents Proected videos.'''
    __tablename__ = 'videos'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    filename = db.Column(db.String(255))
    view = db.Column(db.Integer)
    img_name = db.Column(db.String(255))
    c_time = db.Column(db.DateTime)

    classify_id = db.Column(db.Integer, db.ForeignKey('classifys.id'))

    def __init__(self, _id, name, filename, img):
        self.id = _id
        self.name = name
        self.filename = filename
        self.img_name = img
        self.view = 0
        self.c_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def __repr__(self):
        '''Define the string format for instance of Video.'''
        return "<Model Video '{}'>".format(self.name)


# 分类
class Classify(db.Model):
    '''Represents Proected tags.'''
    __tablename__ = 'classifys'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    videos = db.relationship('Video', backref='classify')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        '''Define the string format for instance of Classify.'''
        return "<Model Classify '{}'>".format(self.name)
