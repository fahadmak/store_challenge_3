import unittest

from app import create_app
from app.models.database import Database


class TestProductApi(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])

    def test_insert_user(self):
        inserted = self.db.create_user('fahad', 'manny', 'manny09')
        retrieve = self.db.get_item('users', 'username', 'manny')
        assert retrieve[2] == 'manny'

    def test_insert_category(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        retrieve = self.db.get_item('categories', 'category_name', 'food')
        assert retrieve[1] == 'food'

    def test_insert_product(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        retrieve = self.db.get_item('products', 'product_name', 'beans')
        assert retrieve[1] == 'beans'

    def test_modify_category(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        modify = self.db.modify_category('junk', 1)
        retrieve = self.db.get_item('categories', 'category_id', 1)
        assert retrieve[1] == 'junk'

    def test_delete_category(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        delete = self.db.delete_category(1)
        retrieve = self.db.get_item('categories', 'category_id', 1)
        assert retrieve is None

    def test_modify_product(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        modify = self.db.modify_product('junk', 20, 400, 1)
        retrieve = self.db.get_item('products', 'product_id', 1)
        assert retrieve[1] == 'junk'

    def test_delete_product(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        delete = self.db.delete_product(1)
        retrieve = self.db.get_item('products', 'product_id', 1)
        assert retrieve is None

    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')