import mock

from flask import url_for
from flask_login import current_user

from alfred.database import db
from alfred_db.models import User

from .base import DatabaseTestCase, href


class AuthTestCase(DatabaseTestCase):

    def setUp(self):
        self.callback_url = href(url_for('auth.callback'), code='testcode')
        self.oauth2_patcher = mock.patch(
            'alfred.views.auth.get_oauth2_handler',
        )
        self.get_oauth2_handler = self.oauth2_patcher.start()
        self.get_oauth2_handler().get_token.return_value = {
            'access_token': ['token']
        }
        self.mock_github()

    def tearDown(self):
        self.oauth2_patcher.stop()
        self.github_patcher.stop()

    def mock_github(self):
        self.github_patcher = mock.patch('alfred.helpers.Github')
        self.github = self.github_patcher.start()
        self.github_api = self.github.return_value
        github_user = mock.Mock()
        github_user.id = '1000'
        github_user.name = 'Bender Rodrigues'
        github_user.login = 'bender'
        github_user.email = 'bender@futurama.fox'
        self.github_api.get_user.return_value = github_user

    def test_user_in_context(self):
        self.client.get('/')
        context_user = self.get_context_variable('current_user')
        self.assertEqual(context_user, current_user)

    def test_callback_redirect(self):
        response = self.client.get(self.callback_url)
        self.assertRedirects(response, url_for('web.index'))

    def test_token_response(self):
        self.client.get(self.callback_url)
        self.get_oauth2_handler().get_token.assert_called_with('testcode')

    def test_github_api_call(self):
        self.client.get(self.callback_url)
        self.github.assert_called_with('token')

    @mock.patch('alfred.helpers.generate_apitoken')
    def test_user_attrs(self, generate_apitoken):
        generate_apitoken.return_value = 'RANDOM'
        self.client.get(self.callback_url)
        user = db.session.query(User).filter_by(github_id='1000').first()
        self.assertIsNotNone(user)
        generate_apitoken.assertCalledWith('token')
        self.assertEqual(user.login, 'bender')
        self.assertEqual(user.name, 'Bender Rodrigues')
        self.assertEqual(user.email, 'bender@futurama.fox')
        self.assertEqual(user.github_access_token, 'token')
        self.assertEqual(user.apitoken, 'RANDOM')

    @mock.patch('alfred.views.auth.login_user')
    def test_user_logged_in(self, login_user):
        self.client.get(self.callback_url)
        user = db.session.query(User).filter_by(github_id='1000').first()
        login_user.assert_called_with(user)
