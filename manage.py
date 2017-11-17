from videoonline import create_app, models
from flask_script import Server, Manager
from flask_migrate import Migrate, MigrateCommand

import os

# Get the ENV from os_environ
env = os.environ.get('env', 'Dev')

# Create thr app instance via Factory Method
app = create_app('videoonline.config.%sConfig' % env.capitalize())

# Init manager object via app object
manager = Manager(app)

# Init migrate object via app and db object
migrate = Migrate(app, models.db)

# Create a new commands: server
# This command will be run the Flask development_env server
manager.add_command("server", Server(host='127.0.0.1', port=3000))
manager.add_command("db", MigrateCommand)

@manager.shell
def make_shell_context():
    """Create a python CLI.

    return: Default import object
    type: `Dict`
    """
    # 确保有导入 Flask app object，否则启动的 CLI 上下文中仍然没有 app 对象
    return dict(
        app=app,
        db=models.db,
        User=models.User,
        Video=models.Video,
        Classify=models.Classify,
        Role=models.Role,
        Server=Server,
    )


if __name__ == '__main__':
    manager.run()
