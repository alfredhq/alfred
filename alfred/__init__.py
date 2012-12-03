from flask import Flask

from .assets import gears
from .auth import login_manager
from .config import configure
from .database import db
from .views.auth import auth
from .views.web import web
from .views.tasks import tasks


def create_app(config):
    app = Flask(__name__)
    configure(app, config)

    db.init_app(app)
    gears.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(tasks, url_prefix='/tasks')
    app.register_blueprint(web)

    return app
