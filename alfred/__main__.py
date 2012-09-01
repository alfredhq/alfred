#!/usr/bin/env python

import os
from argh import arg, ArghParser
from functools import wraps


DIR = os.path.abspath(os.path.dirname(__file__))
CONFIG = os.path.join(DIR, 'configs', 'default.yml')
CONFIG = os.environ.get('ALFRED_CONFIG', CONFIG)


def with_app(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from alfred import create_app
        app = create_app(CONFIG)
        return func(app, *args, **kwargs)
    return wrapper


@arg('--host', default='127.0.0.1', help='the host')
@arg('--port', default=5000, help='the port')
@with_app
def runserver(app, args):
    app.run(args.host, args.port)


@with_app
def shell(app, args):
    from alfred.helpers import get_shell
    with app.test_request_context():
        sh = get_shell()
        sh(app=app)


@with_app
def collectassets(app, args):
    from flask_gears import Gears
    Gears().get_environment(app).save()


def main():
    parser = ArghParser()
    parser.add_commands([runserver, shell, collectassets])
    parser.dispatch()


if __name__ == '__main__':
    main()
