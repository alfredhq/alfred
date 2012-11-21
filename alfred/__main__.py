#!/usr/bin/env python

import os
from argh import arg, ArghParser
from argh.exceptions import CommandError
from functools import wraps


CONFIG = os.environ.get('ALFRED_CONFIG')


def with_app(func):
    @wraps(func)
    @arg('--config', help='path to config')
    def wrapper(args):
        from alfred import create_app
        if not CONFIG and not args.config:
            raise CommandError('There is no config file specified')
        app = create_app(args.config or CONFIG)
        return func(app, args)
    return wrapper


@arg('--host', default='127.0.0.1', help='the host')
@arg('--port', default=5000, help='the port')
@arg('--noreload', action='store_true', help='disable code reloader')
@with_app
def runserver(app, args):
    app.run(args.host, args.port, use_reloader=not args.noreload)


@with_app
def shell(app, args):
    from alfred.helpers import get_shell
    with app.test_request_context():
        sh = get_shell()
        sh(app=app)


@with_app
def collectassets(app, args):
    from alfred.assets import gears
    gears.get_environment(app).save()


def main():
    parser = ArghParser()
    parser.add_commands([runserver, shell, collectassets])
    parser.dispatch()


if __name__ == '__main__':
    main()
