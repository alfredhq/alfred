import os
import unittest2

from alfred_db.models import Base
from alfred import create_app
from alfred.database import db


TESTS_DIR = os.path.dirname(__file__)
FIXTURES_DIR = os.path.join(TESTS_DIR, 'fixtures')
CONFIG = os.path.join(TESTS_DIR, 'config.yml')


class BaseTestCase(unittest2.TestCase):

    def __call__(self, result=None):
        try:
            self._pre_setup()
            with self.client:
                super(BaseTestCase, self).__call__(result)
        finally:
            self._post_teardown()

    def _pre_setup(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_teardown(self):
        if getattr(self, '_ctx', None) is not None:
            self._ctx.pop()

    def setUp(self):
        Base.metadata.create_all(bind=db.engine)

    def tearDown(self):
        db.session_class.remove()
        Base.metadata.drop_all(bind=db.engine)

    def create_app(self):
        return create_app(CONFIG)
