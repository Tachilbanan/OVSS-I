from flask import Flask, render_template
from videoonline import models
from videoonline.models import db
from videoonline.extensions import bcrypt, login_manager, principals
from flask_principal import identity_loaded, UserNeed, RoleNeed
from flask_login import current_user

def Create_App(Config = 'videoonline.config.DevConfig'):
    app = Flask(__name__)
    with app.app_context():
        app.config.from_object(Config)

        # Will be load the SQLALCHEMY_DATABASE_URL from config.py to db object
        db.init_app(app)
        # 数据库是一个重要的组件，所以先把数据库内容全部完成再继续后面的操作


        # Init the Flask-Bcrypt via app object
        bcrypt.init_app(app)
        # Init the Flask-Login via app object
        login_manager.init_app(app)
        # Init the Flask-Prinicpal via app object
        principals.init_app(app)

        # 因为 identity_loaded 信号实现函数,需要访问 app 对象, 所以直接在 create_app() 中实现.
        @identity_loaded.connect_via(app)
        def on_identity_loaded(sender, identity):
            """Change the role via add the Need object into Role.

               Need the access the app object.
            """

            # Set the identity user object
            identity.user = current_user

            # Add the UserNeed to the identity user object
            if hasattr(current_user, 'id'):
                identity.provides.add(UserNeed(current_user.id))

            # Add each role to the identity user object
            if hasattr(current_user, 'roles'):
                # 原本多对多的用户权限，现在改成用户对应角色 一对多，取消for循环
                # for role in current_user.roles:
                role = current_user.roles
                identity.provides.add(RoleNeed(role.name))

        app.static_folder = 'theme/static'
        app.template_folder = 'theme/templates'

        # 定义 404，405 等、这里只定义 404
        @app.errorhandler(404)
        def page_not_found(error):
            return render_template('40X/404.html'), 404

        from videoonline.view import root_view
        from videoonline.admin import admin_view

        app.register_blueprint(root_view, url_prefix = '/')
        app.register_blueprint(admin_view, url_prefix = '/admin')

        return app
