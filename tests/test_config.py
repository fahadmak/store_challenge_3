import unittest
from app import create_app


class TestDevelopmentConfig(unittest.TestCase):

    def test_app_is_development(self):
        app = create_app("development")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertEqual(
            app.config['DATABASE_URI'], 'postgres://tquvntrciomlye:0e9dfeca2f405e0f2193a3b7fbc6f316dd4f63caad0fdf9b5a4406bcb2fbc585@ec2-23-21-171-249.compute-1.amazonaws.com:5432/d1akcs0pg5u19u'
        )
        self.assertTrue(app.config['JWT_SECRET_KEY'] == 'bigsecret')

    def test_app_is_testing(self):
        app = create_app("testing")
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(app.config['TESTING'] is True)
        self.assertTrue(
            app.config['DATABASE_URI'] == 'postgresql://postgres:maka1997@localhost/testdb'
        )
