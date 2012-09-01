from flask import Flask
from flask_gears import Gears

from .auth import login_manager
from .config import configure
from .database import db
from .views.auth import auth
from .views.web import web


def create_app(config):
    app = Flask(__name__)
    configure(app, config)

    db.init_app(app)
    login_manager.init_app(app)
    Gears(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(web)

    return app
