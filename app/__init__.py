from flask import Flask
from config import config

# init Redis db
from .utils import Redis
rredis=Redis.connect()
rredis.flushdb()

# init SQL db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask_apscheduler import APScheduler
scheduler=APScheduler()
from .tasks import *


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.jinja_env.variable_start_string = "{{ "
    app.jinja_env.variable_end_string = " }}"
    scheduler.init_app(app)
    # scheduler.add_job(func=task1, id='1', trigger='interval', seconds=10, replace_existing=True)
    scheduler.start()
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app