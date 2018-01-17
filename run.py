# -*- coding:utf-8 -*-
from app import create_app, db
from app import models
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


# 创建shell上下文环境
def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()