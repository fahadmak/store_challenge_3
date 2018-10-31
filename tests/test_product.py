import unittest
import json

from app import create_app
from app.models.database import Database


class TestProduct(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        self.token = json.loads(response1.data)['access_token']
        post_add = dict(category_name="Fahad2344")
        response = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})

    def test_add_product(self):
        post_add = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response2 = self.app.post('/api/v1/categories/1/products', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response2.data)['message'] == 'Fahad2344 has successfully been added to inventories'
        assert response2.status_code == 201
        assert response2.headers["Content-Type"] == "application/json"

    def test_add_product_no_rights(self):
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + self.token})
        login = dict(username="Giga", password="Shoort")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        datoken = json.loads(response1.data)['access_token']
        post_add = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response2 = self.app.post('/api/v1/categories/1/products', json=post_add,
                                 headers={'Authorization': 'Bearer ' + datoken})
        assert json.loads(response2.data)['error'] == "you do not have admin rights"
        assert response2.status_code == 403
        assert response2.headers["Content-Type"] == "application/json"

    def test_create_user_invalid_content(self):
        post_add = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response = self.app.post('/api/v1/categories/1/products', json=post_add, content_type='application/javascript',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'Invalid content type'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_empty_fields(self):
        post_add = dict(product_name="Fahad2344", quantity=12)
        response = self.app.post('/api/v1/categories/1/products', json=post_add, content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == {'error': {'product_price': ['required field']}}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_incorrect_input(self):
        post_add = dict(product_name=50, quantity=12, product_price=34)
        response = self.app.post('/api/v1/categories/1/products', json=post_add, content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == {'error': {'product_name': ['must be of string type']}}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_already_exists(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1= self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        post_add = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response2 = self.app.post('/api/v1/categories/1/products', json=post_add,
                                  headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response2.data) == {'error': 'Fahad2344 already exists'}
        assert response2.status_code == 400
        assert response2.headers["Content-Type"] == "application/json"

    def test_modify_product(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(product_name="Freddd", quantity=120, product_price=90)
        response = self.app.put('/api/v1/categories/1/products/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['message'] == 'Freddd has successfully been modified'
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_product_no_rights(self):
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + self.token})
        login = dict(username="Giga", password="Shoort")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        datoken = json.loads(response1.data)['access_token']
        put_add = dict(product_name="Freddd", quantity=120, product_price=90)
        response = self.app.put('/api/v1/categories/1/products/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + datoken})
        assert json.loads(response.data)['error'] == 'you do not have admin rights'
        assert response.status_code == 403
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_product_invalid_content(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(product_name="Freddd", quantity=120, product_price=90)
        response = self.app.put('/api/v1/categories/1/products/1', json=put_add,
                                content_type='application/javascript',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'Invalid content type'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_product_field_empty(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(product_name="Fahad2344", quantity=12)
        response = self.app.put('/api/v1/categories/1/products/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error']['error'] == {'product_price': ['required field']}
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_product_invalid_input(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(product_name="Fahad2344", quantity="fish")
        response = self.app.put('/api/v1/categories/1/products/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error']['error']['quantity'] == ['must be of integer type']
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_modify_product_already_exists(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        put_add = dict(product_name="Fahad2344", quantity=120, product_price=90)
        response = self.app.put('/api/v1/categories/1/products/1', json=put_add,
                                headers={'Authorization': 'Bearer ' + self.token})
        assert "Fahad2344 name already exists" in json.loads(response.data)['error']
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_delete_product(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        response = self.app.delete('/api/v1/categories/1/products/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['message'] == 'Product has been deleted'
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_delete_no_product(self):
        response = self.app.delete('/api/v1/categories/1/products/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data) == {'error': 'product does not exist'}
        assert response.status_code == 404
        assert response.headers["Content-Type"] == "application/json"

    def test_get_product_by_id(self):
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12)
        response1 = self.app.post('/api/v1/categories/1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        response = self.app.get('/api/v1/categories/1/products/1', content_type='application/json',
                                   headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['product']['name'] == 'Fahad2344'
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"

    def test_get_product_by_id_does_not_exist(self):
        response = self.app.get('/api/v1/categories/1/products/1', content_type='application/json',
                                headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'product does not exist'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')
        self.db.drop_tables('sales')
        self.db.drop_tables('sold')