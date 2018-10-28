import unittest
import json

from app import create_app
from app.models.database import Database


class TestProductApi(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])

    def test_product_content_type(self):
        post_signup = dict(name="Fahad", price=12)
        response = self.app.post('/api/v1/products', json=post_signup, content_type='application/javascript')
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "Invalid content type" in str(response.data)

    def test_empty_fields(self):
        post_signup = dict()
        response = self.app.post('/api/v1/products', json=post_signup)
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "empty price field" in json.loads(response.data)['error']['price']

    def test_incorrect_input(self):
        post_signup = dict(name=1, price="fahad", quantity="12")
        response = self.app.post('/api/v1/products', json=post_signup)
        # assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"
        assert "incorrect username format" == json.loads(response.data)['error']['name']

    def test_product_already_exists(self):
        post_signup = dict(name="Fahad", price=12, quantity=12)
        post_signup2 = dict(name="Fahad", price=120, quantity=16)
        response = self.app.post('/api/v1/products', json=post_signup)
        response2 = self.app.post('/api/v1/products', json=post_signup2)
        assert response2.status_code == 400
        assert response2.headers["Content-Type"] == "application/json"
        assert "Fahad already exists" in str(response2.data)

    # Tests for get all products

    def test_get_all_products(self):
        post_signup = dict(name="Fahad", price=12, quantity=12)
        post_signup2 = dict(name="Jowe", price=120, quantity=16)
        response = self.app.post('/api/v1/products', json=post_signup)
        response2 = self.app.post('/api/v1/products', json=post_signup2)
        response3 = self.app.get('/api/v1/products')
        assert response3.status_code == 200
        assert response3.headers["Content-Type"] == "application/json"
        assert "Fahad" and "Jowe" in str(response3.data)

    def test_no_products(self):
        response3 = self.app.get('/api/v1/products')
        assert "There currently no products" in str(response3.data)
        assert response3.status_code == 200
        assert response3.headers["Content-Type"] == "application/json"

    def test_get_product_by_id(self):
        post_signup = dict(name="Fahad", price=12, quantity=12)
        response = self.app.post('/api/v1/products', json=post_signup)
        response1 = self.app.get('/api/v1/products/1')
        assert response1.status_code == 200
        assert response1.headers["Content-Type"] == "application/json"
        assert "Fahad" in str(response1.data)

    def test_product_of_id_does_not_exist(self):
        response2 = self.app.get('/api/v1/products/1')
        assert response2.status_code == 404
        assert response2.headers["Content-Type"] == "application/json"
        assert "product of ID 1 does not exist" in str(response2.data)

