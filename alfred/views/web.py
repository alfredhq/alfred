from flask import Blueprint, render_template


web = Blueprint('web', __name__)


@web.route('/')
def index():
    return render_template('index.html')
