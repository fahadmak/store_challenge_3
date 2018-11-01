import unittest
from app import create_app


class TestDevelopmentConfig(unittest.TestCase):

    def test_app_is_development(self):
        app = create_app("development")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertEqual(
            app.config['DATABASE_URI'], 'postgresql://postgres:maka1997@localhost/storedb'
        )
        self.assertTrue(app.config['JWT_SECRET_KEY'] == 'bigsecret')

    def test_app_is_testing(self):
        app = create_app("testing")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertTrue(
            app.config['DATABASE_URI'] == 'postgresql://postgres:maka1997@localhost/testdb'
        )
