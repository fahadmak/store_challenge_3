import unittest
import json

from app import create_app
from app.models.database import Database


class TestUser(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])

    def test_create_user(self):
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/signup', json=post_signup)
        assert json.loads(response.data)['message'] == "Giga has successfully been added to staff"
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_empty_fields(self):
        post_signup = dict()
        response = self.app.post('/api/v1/auth/signup', json=post_signup)
        assert json.loads(response.data)['error']['name'] == 'empty name field'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_incorrect_input(self):
        post_signup = dict(name=7, username=7, password=7)
        response = self.app.post('/api/v1/auth/signup', json=post_signup)
        assert json.loads(response.data)['error']['username'] == "incorrect username format"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_already_exists(self):
        post_signup1 = dict(name="Fahad", username="Giga", password="Shoort")
        response1 = self.app.post('/api/v1/auth/signup', json=post_signup1)
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/signup', json=post_signup)
        assert json.loads(response.data)['error'] == "Giga already exists"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"


    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')