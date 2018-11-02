import unittest
import json

from app import create_app
from app.models.database import Database


class TestSales(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])
        login = dict(username="admin", password="admin")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        self.token = json.loads(response1.data)['access_token']

    def test_create_sale(self):
        post_signup = dict(name="Fahad", username="Giga", password="Shoort")
        response = self.app.post('/api/v1/auth/signup', json=post_signup,
                                 headers={'Authorization': 'Bearer ' + self.token})
        login = dict(username="Giga", password="Shoort")
        response1 = self.app.post('/api/v1/auth/login', json=login)
        token = json.loads(response1.data)['access_token']
        post_add = dict(category_name="phill")
        response1 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + token})
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12, category_id=1)
        response2 = self.app.post('/api/v1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + token})
        sale = dict(product_id=1, quantity=10)
        response4 = self.app.post('/api/v1/sales', json=sale,
                                 headers={'Authorization': 'Bearer ' + token})
        assert json.loads(response4.data)['error'] == 'you should be a sale attendant'
        assert response4.status_code == 401
        assert response4.headers["Content-Type"] == "application/json"

    def test_create_sale_low_quantity(self):
        post_add = dict(category_name="phill")
        response1 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12, category_id=1)
        response2 = self.app.post('/api/v1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        sale = dict(product_id=1, quantity=100)
        response = self.app.post('/api/v1/sales', json=sale,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == 'This quantity is unavailable, try lesser quantity'
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_create_empty(self):
        post_add = dict(category_name="phill")
        response1 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12, category_id=1)
        response2 = self.app.post('/api/v1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        sale = dict(product_id=1)
        response = self.app.post('/api/v1/sales', json=sale,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error'] == {'error': {'quantity': ['required field']}}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_create_sale_incorrect_input(self):
        post_add = dict(category_name="phill")
        response1 = self.app.post('/api/v1/categories', json=post_add,
                                 headers={'Authorization': 'Bearer ' + self.token})
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12, category_id=1)
        response2 = self.app.post('/api/v1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        sale = dict(product_id=1, quantity="food")
        response = self.app.post('/api/v1/sales', json=sale,
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response.data)['error']['error'] == {'quantity': ['must be of integer type']}
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

    def test_get_sale_by_id_admin(self):
        post_add = dict(category_name="phill")
        response1 = self.app.post('/api/v1/categories', json=post_add,
                                  headers={'Authorization': 'Bearer ' + self.token})
        post_add2 = dict(product_name="Fahad2344", quantity=12, product_price=12, category_id=1)
        response2 = self.app.post('/api/v1/products', json=post_add2,
                                  headers={'Authorization': 'Bearer ' + self.token})
        sale = dict(product_id=1, quantity=10)
        response = self.app.post('/api/v1/sales', json=sale,
                                 headers={'Authorization': 'Bearer ' + self.token})
        response3 = self.app.get('/api/v1/sales/1', content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response3.data)['sale']['sale_id'] == 1
        assert response3.status_code == 200
        assert response3.headers["Content-Type"] == "application/json"

    def test_get_all_sale(self):

        response3 = self.app.get('/api/v1/sales', content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response3.data) == {'error': 'you do not have admin rights'}
        assert response3.status_code == 401
        assert response3.headers["Content-Type"] == "application/json"

    def test_no_sales(self):
        response3 = self.app.get('/api/v1/sales', content_type='application/json',
                                   headers={'Authorization': 'Bearer ' + self.token})
        assert json.loads(response3.data) == {'error': 'you do not have admin rights'}
        assert response3.status_code == 401
        assert response3.headers["Content-Type"] == "application/json"

    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')
        self.db.drop_tables('sales')
        self.db.drop_tables('sold')