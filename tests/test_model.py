import unittest

from app.models.user_model import User, users
from app.models.product_model import Product, products


class TestModel(unittest.TestCase):
    def setUp(self):
        self.user = User
        self.users = users
        self.user1 = self.user(1, "benwa", "real", "real", "tuesday 2018", True)
        self.user2 = self.user(2, "meshu", "trdff", "tres", "tuesday 2018", True)
        self.users = [self.user1, self.user2]
        self.product = Product
        self.products = products
        self.product1 = self.product(1, "benwa", 5000, 20)
        self.product2 = self.product(2, "meshu", 8000, 30)
        self.products = [self.product1, self.product2]

    def test_create_product(self):
        assert isinstance(self.product1, self.product)
        assert self.product1.product_name == "benwa"
        assert self.product1.price == 20

    def test_product_to_json(self):
        product_json = self.product1.to_json()
        assert isinstance(product_json, dict)
        assert product_json == {"productId": 1, "name": "benwa", "price": 20, "quantity": 5000}

    def test_create_user(self):
        assert isinstance(self.user1, self.user)
        assert self.user1.name == "benwa"

    def test_user_to_json(self):
        user_json = self.user1.to_json()
        assert isinstance(user_json, dict)
