import unittest

from app import create_app
from app.models.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])

    def test_insert_user(self):
        inserted = self.db.create_user('fahad', 'manny', 'manny09')
        retrieve = self.db.find_user_by_username('manny')
        assert retrieve.username == 'manny'

    def test_insert_category(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        retrieve = self.db.find_category_by_category_name('food')
        assert retrieve.category_name == 'food'

    def test_insert_product(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        retrieve = self.db.find_product_by_product_name('beans')
        assert retrieve.product_name == 'beans'

    def test_modify_category(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        modify = self.db.modify_category('junk', 1)
        retrieve = self.db.find_category_by_category_id(1)
        assert retrieve.category_name == 'junk'

    def test_delete_category(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        delete = self.db.delete_category(1)
        retrieve = self.db.find_category_by_category_id(1)
        assert retrieve is None

    def test_modify_product(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        modify = self.db.modify_product('junk', 20, 400, 1)
        retrieve = self.db.find_product_by_product_id(1)
        assert retrieve.product_name == 'junk'

    def test_delete_product(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        delete = self.db.delete_product(1)
        retrieve = self.db.find_product_by_product_id(1)
        assert retrieve is None

    def test_get_all(self):
        insert = self.db.create_user('fahad', 'manny', 'manny09')
        inserted = self.db.add_category('food', 1)
        final_insert = self.db.add_product('beans', 200, 300, 1, 1)
        third = self.db.add_sale(100, 1)
        find_user = self.db.find_user_by_id(1)
        rights = self.db.modify_admin_rights(1)
        user_id = self.db.find_sale_by_user_id(1)
        retrieve = self.db.find_sale_by_sale_id(1)
        sales = self.db.get_all_sales()
        categories = self.db.get_all_categories()
        products = self.db.get_all_products()
        assert find_user.is_admin is True
        assert retrieve.user_id == 1
        assert retrieve.sale_id == 1
        assert isinstance(sales, list)
        assert isinstance(categories, list)
        assert isinstance(products, list)

    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')