import os
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_app, db
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand) #添加db 命令（runserver的用法）
manager.run()
# if __name__ == '__main__':
#     app.run(host='127.0.0.1', port=8080, debug=True)
