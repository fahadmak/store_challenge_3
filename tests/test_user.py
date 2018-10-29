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

    def test_create_user_invalid_content(self):
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/signup', json=post_signup, content_type='application/javascript')
        assert json.loads(response.data)['error'] == "Invalid content type"
        assert response.status_code == 400
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

    def test_login(self):
        post_signup1 = dict(name="Fahad", username="Giga", password="Shoort")
        response1 = self.app.post('/api/v1/auth/signup', json=post_signup1)
        login = dict(username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data)['message'] == "login successful"
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_login_invalid_content(self):
        login = dict(username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/login', json=login, content_type='application/javascript')
        assert json.loads(response.data)['error'] == "Invalid content type"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login_password_no_match(self):
        post_signup1 = dict(name="Fahad", username="Giga", password="Shoort")
        response1 = self.app.post('/api/v1/auth/signup', json=post_signup1)
        login = dict(username="Giga", password="Shoort3")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data)['error'] == "Username and password did not match"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login_username_doesnot_exist(self):
        login = dict(username="Gigar", password="Shoort3")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data)['error'] == "username doesn't exist"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login_empty(self):
        login = dict()
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data)['error']['password'] == 'empty quantity field'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login_incorrect(self):
        login = dict(username=7, password="Shoort3")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data)['error']['username'] == 'incorrect username format'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"


    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')