from alfred_db.models import User
from flask import current_app
from github import Github
from requests_oauth2 import OAuth2

from .database import db


def get_shell():
    try:
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
    except ImportError:
        import code
        return lambda **context: code.interact('', local=context)
    else:
        ipython = InteractiveShellEmbed(banner1='')
        return lambda **context: ipython(global_ns={}, local_ns=context)


def get_oauth2_handler():
    GITHUB = current_app.config['GITHUB']
    return OAuth2(
        client_id=GITHUB['client_id'],
        client_secret=GITHUB['client_secret'],
        site=GITHUB['auth_url'],
        redirect_uri='',
        authorization_url=GITHUB['authorization_url'],
        token_url=GITHUB['token_url']
    )


def get_user_by_token(access_token):
    api = Github(access_token)
    github_user = api.get_user()
    user = db.session.query(User).filter_by(github_id=github_user.id).first()
    if user is None:
        user = User(
            github_access_token=access_token,
            github_id=github_user.id,
            name=github_user.name,
            email=github_user.email,
            login=github_user.login,
        )
        db.session.add(user)
    else:
        user.github_access_token = access_token
        user.login = github_user.login
    db.session.commit()
    return user
