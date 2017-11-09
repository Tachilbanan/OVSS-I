from flask_sqlalchemy import SQLAlchemy
from videoonline.extensions import bcrypt

db = SQLAlchemy()

# # 用户-权限 多对多关系声明
# users_roles = db.Table('users_roles',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
#     db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

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
        self.roles = helper

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
    users = db.relationship('User', backref='roles')

    def __init__(self, name):
        # self.id = id
        self.name = name

    def __repr__(self):
        return "<Model Role `{}`>".format(self.name)

# 视频-分类 多对多关系声明
videos_classifys = db.Table('videos_classifys',
                      db.Column('video_id', db.String(45), db.ForeignKey('videos.id')),
                      db.Column('classify_id', db.String(45), db.ForeignKey('classifys.id')))

# 视频
class Video(db.Model):
    '''Represents Proected videos.'''
    __tablename__ = 'videos'

    id = db.Column(db.String(255), primary_key = True)
    name = db.Column(db.String(255))
    publish_date = db.Column(db.DateTime)
    # many to many: videos <==> classifys
    classifys = db.relationship(
        'Classify',
        secondary = videos_classifys,
        backref = db.backref('videos', lazy='dynamic'))

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        '''Define the string format for instance of Video.'''
        return "<Model Video '{}'>".format(self.name)

# 分类
class Classify(db.Model):
    '''Represents Proected tags.'''
    __tablename__ = 'classifys'

    id = db.Column(db.String(45), primary_key = True)
    name = db.Column(db.String(255))

    def __repr__(self):
        '''Define the string format for instance of Classify.'''
        return "<Model Classify '{}'>".format(self.name)