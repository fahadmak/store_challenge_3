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
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(name="Fahad", username="igaa4", password="hoort3")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['message'] == "igaa4 has successfully been added to staff"
        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/json"

    def test_create_user_invalid_content(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(name="Fahad", username="igaa4", password="hoort3")
        response = self.app.post('/api/v1/auth/signup', json=post_signup, content_type='application/javascript',
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == "Invalid content type"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_empty_fields(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(username="admin4", password="admin4")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == {'error': {'name': ['required field']}}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_incorrect_input(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(name=7, username="reat4", password="retty5")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == {'error': {'name': ['must be of string type']}}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_already_exists(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup2 = dict(name="Fahad", username="igaa4", password="hoort3")
        response2 = self.app.post('/api/v1/auth/signup', json=post_signup2,
                                  headers={'Authorization': 'Bearer ' + token})
        post_signup = dict(name="Fahad", username="igaa4", password="hoort3")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == "igaa4 already exists"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login(self):
        login = dict(username="admin", password="admin")
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
        login = dict(username="admin", password="hoort4")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data)['error'] == "Username and password did not match"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login_empty(self):
        login = dict(password="hoort3")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data) == {'username': ['required field']}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_login_incorrect(self):
        login = dict(username=7, password="hoort3")
        response = self.app.post('/api/v1/auth/login', json=login)
        assert json.loads(response.data) == {'username': ['must be of string type']}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_rights(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(name="Fahad", username="igaa4", password="hoort3")
        response2 = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        response = self.app.put('/api/v1/auth/promote/2', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['message'] == "igaa4 is now an admin"
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_already_has_rights(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(name="Fahad", username="igaa3", password="hoort2")
        response2 = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        response3 = self.app.put('/api/v1/auth/promote/2', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        response = self.app.put('/api/v1/auth/promote/2', json=post_signup,
                                headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == "igaa3 already has admin rights"
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_rights_doesnot_exist(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response2 = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + token})
        response = self.app.put('/api/v1/auth/promote/4', json=post_signup,
                                headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == "User does not exist"
        assert response.status_code == 404
        assert response.headers["Content-Type"] == "application/json"

    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')
        self.db.drop_tables('sales')
        self.db.drop_tables('sold')