import unittest2

from alfred import helpers


class HelpersTestCase(unittest2.TestCase):

    def test_token_generator(self):
        self.assertEqual(len(helpers.generate_apitoken('token')), 40)
