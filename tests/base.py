import os
import unittest2

from flask import template_rendered
from werkzeug import Href

from alfred import create_app
from alfred_db.models import Base
from alfred.database import db


TESTS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')
if os.environ.get('TRAVIS'):
    CONFIG = os.path.join(TESTS_DIR, 'travis.yml')
else:
    CONFIG = os.path.join(TESTS_DIR, 'config.yml')


class ContextVariableDoesNotExist(Exception):
    pass


class ApplicationTestCase(unittest2.TestCase):

    def __call__(self, result=None):
        try:
            self._pre_setup()
            with self.client:
                super(ApplicationTestCase, self).__call__(result)
        finally:
            self._post_teardown()

    def _pre_setup(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

        self.templates = []
        template_rendered.connect(self._add_template)

    def _post_teardown(self):
        if getattr(self, '_ctx', None) is not None:
            self._ctx.pop()
        template_rendered.disconnect(self._add_template)

    def _add_template(self, app, template, context):
        self.templates.append((template, context))

    def create_app(self):
        return create_app(CONFIG)

    def get_context_variable(self, name):
        for template, context in self.templates:
            if name in context:
                return context[name]
        raise ContextVariableDoesNotExist

    def assertContext(self, name, value):
        try:
            self.assertEqual(self.get_context_variable(name), value)
        except ContextVariableDoesNotExist:
            self.fail('Context variable does not exist: %s' % name)

    def assertTemplateUsed(self, name):
        if not any(t.name == name for t, c in self.templates):
            self.fail('Template %s is not used' % name)

    def assertRedirects(self, response, location, status_code=None):
        if status_code is not None:
            self.assertEqual(response.status_code, status_code)
        else:
            self.assertIn(response.status_code, (301, 302))
        self.assertEqual(response.location, 'http://localhost' + location)


class DatabaseTestCase(ApplicationTestCase):

    def _pre_setup(self):
        super(DatabaseTestCase, self)._pre_setup()
        Base.metadata.create_all(bind=db.engine)

    def _post_teardown(self):
        if self.app is not None:
            db.session_class.remove()
            Base.metadata.drop_all(bind=db.engine)
        super(DatabaseTestCase, self)._post_teardown()


def href(path, **query):
    return Href(path)(**query)
