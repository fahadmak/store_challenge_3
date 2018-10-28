import unittest
import json

from app import create_app
from app.models.database import Database


class TestUser(unittest.TestCase):
    def setUp(self):
        app = create_app("testing")
        self.app = app.test_client()
        self.db = Database(app.config['DATABASE_URI'])


    def tearDown(self):
        self.db.drop_tables('users')
        self.db.drop_tables('products')
        self.db.drop_tables('categories')