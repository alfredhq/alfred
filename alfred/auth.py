from alfred_db.models import User
from flask_login import LoginManager
from .database import db


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(id):
    db.session.query(User).get(id)
