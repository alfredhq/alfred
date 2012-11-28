import hashlib
import urllib

from flask import Blueprint, request, redirect, url_for, current_app
from flask_login import login_user, logout_user

from ..helpers import get_oauth2_handler, get_user_by_token


auth = Blueprint('auth', __name__)


@auth.route('/callback/')
def callback():
    oauth2_handler = get_oauth2_handler()
    code = request.args.get('code')
    response = oauth2_handler.get_token(code)
    if 'access_token' not in response:
        return redirect(url_for('web.index'))
    access_token = response['access_token'][0]
    user = get_user_by_token(access_token)
    if user:
        login_user(user)
    return redirect(url_for('web.index'))


@auth.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('web.index'))


@auth.app_context_processor
def inject_auth_url():
    oauth2_handler = get_oauth2_handler()
    auth_url = oauth2_handler.authorize_url(
        current_app.config['GITHUB']['scopes']
    )
    return {'auth_url': auth_url}


@auth.app_context_processor
def gravatar_processor():
    def gravatar_url(email, size, default='identicon'):
        gravatar_url = 'http://www.gravatar.com/avatar/'
        hash = hashlib.md5(email.lower()).hexdigest()
        params = urllib.urlencode({'s': str(size), 'd': default})
        return '{host}{hash}?{params}'.format(
            host=gravatar_url,
            hash=hash,
            params=params,
        )
    return {'gravatar_url': gravatar_url}
