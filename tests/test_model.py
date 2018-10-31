import unittest

from app.models.user_model import User, users
from app.models.product_model import Product, products
from app.models.sale_model import Sale, sales, Sold
from app.models.category_model import Category, categories


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
        self.category = Category
        self.cat1 = self.category(1, 'free', 1)
        self.cats = categories
        self.cats = [self.cat1]
        self.sale = Sale
        self.sale1 = self.sale(1, 200, 'tuesday 11.29', 1)
        self.sale2 = self.sale(2, 200, 'tuesday 11.50', 1)
        self.sales = sales
        self.sales = [self.sale1, self.sale2]
        self.sold = Sold
        self.sold1 = self.sold(1, 'fish', 23, 1)


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

    def test_create_sale(self):
        assert isinstance(self.sale1, self.sale)
        assert self.sale1.total == 200

    def test_sale_to_json(self):
        sale_json = self.sale1.to_json()
        assert isinstance(sale_json, dict)

    def test_create_sold(self):
        assert isinstance(self.sold1, self.sold)
        assert self.sold1.sale_id == 1

    def test_sold_to_json(self):
        sold_json = self.sold1.to_json()
        assert isinstance(sold_json, dict)

    def test_create_category(self):
        assert isinstance(self.cat1, self.category)
        assert self.cat1.user_id == 1

    def test_category_to_json(self):
        sold_json = self.cat1.to_json()
        assert isinstance(sold_json, dict)
