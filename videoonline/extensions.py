# 散列函数 负责 密码加密 校验等、
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# 登录管理模块 负责 各种复杂的登录功能
from flask_login import LoginManager

login_manager = LoginManager()

# Setup the configuration for login manager.
#     1. Set the login page.
#     2. Set the more stronger auth-protection.
#     3. Show the information when you are logging.
#     4. Set the Login Messages type as `information`.
login_manager.login_view = "admin.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page."
login_manager.login_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
    """Load the user's info."""

    from videoonline.models import User
    return User.query.filter_by(id = user_id).first()

# 身份控制模块 负责各种复杂的身份校验、权限限制等
from flask_principal import Principal, Permission, RoleNeed

# Create the Flask-Principal's instance
principals = Principal()

# 这里设定了 3 种权限, 这些权限会被绑定到 Identity 之后才会发挥作用.
# Init the role permission via RoleNeed(Need).
superadmin_permission = Permission(RoleNeed('superadmin'))
admin_permission = Permission(RoleNeed('admin'))
helper_permission = Permission(RoleNeed('helper'))