from alfred_db.models import User
from flask_login import LoginManager
from .database import db


login_manager = LoginManager()


@login_manager.user_loader
def load_user(id):
    return db.session.query(User).get(id)
