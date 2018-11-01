import unittest
import json

from app import create_app
from app.models.database import Database


class TestCategory(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        self.token = json.loads(response1.data)['access_token']

    def test_add_category(self):
        post_add = dict(category_name="Fahad2344")
        response = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['message'] == 'Fahad2344 has successfully been added to categories'
        assert response.status_code == 201
        assert response.headers["Content-Type"] == "application/json"

    def test_create_user_invalid_content(self):
        post_add = dict(category_name="Fahad2344")
        response = self.app.post('/api/v1/categories', json=post_add, content_type='application/javascript',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'Invalid content type'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_empty_fields(self):
        post_add = dict()
        response = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert 'required field' in str(json.loads(response.data)['error'])
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_incorrect_input(self):
        post_add = dict(category_name=2344)
        response = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert 'must be of string type' in str(json.loads(response.data))
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_already_exists(self):
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_add = dict(category_name="cool")
        resp = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + token})
        response = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response.data)['error'] == 'cool already exists'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_category(self):
        post_add = dict(category_name="Fahad2344")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(category_name="mackay")
        response = self.app.put('/api/v1/categories/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['message'] == 'mackay has successfully been modified'
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_category_invalid_content(self):
        post_add = dict(category_name="Fahad2344")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(category_name="mackay")
        response = self.app.put('/api/v1/categories/1', json=put_add, content_type='application/javascript',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'Invalid content type'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_category_field_empty(self):
        post_add = dict(category_name="Fahad2344")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict()
        response = self.app.put('/api/v1/categories/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error']['error']['category_name'] == ['required field']
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_category_invalid_input(self):
        post_add = dict(category_name="Fahad2344")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                  headers={'Authorization': 'Bearer ' + self.token})
        post_add = dict(category_name=56)
        response = self.app.put('/api/v1/categories/1', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error']['error']['category_name'] == ['must be of string type']
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_category_already_exists(self):
        post_add = dict(category_name="mackay")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(category_name="mackay")
        response = self.app.put('/api/v1/categories/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'mackay name already exists'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_delete_category(self):
        post_add = dict(category_name="Fahad2344")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        response = self.app.delete('/api/v1/categories/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['message'] == 'Fahad2344 has been deleted'
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_delete_no_category(self):
        response = self.app.delete('/api/v1/categories/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'Category does not exist'
        assert response.status_code == 404
        assert response.headers["Content-Type"] == "application/json"

    def test_get_category_by_id(self):
        post_add = dict(category_name="Fahad2344")
        response3 = self.app.post('/api/v1/categories', json=post_add,
                                  headers={'Authorization': 'Bearer ' + self.token})
        response = self.app.get('/api/v1/categories/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['name'] == 'Fahad2344'
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_get_category_by_id_does_not_exist(self):
        response = self.app.get('/api/v1/categories/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'Category does not exist'
        assert response.status_code == 404
        assert response.headers["Content-Type"] == "application/json"

    def test_get_all_categories(self):
        post_add4 = dict(category_name="Fahad2344")
        response4 = self.app.post('/api/v1/categories', json=post_add4,
                                  headers={'Authorization': 'Bearer ' + self.token})
        response = self.app.get('/api/v1/categories', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['categories'][0]['user_id'] == 1
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')
        self.db.drop_tables('sales')
        self.db.drop_tables('sold')