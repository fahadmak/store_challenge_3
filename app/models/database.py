import psycopg2
import sys
from urllib.parse import urlparse
from passlib.hash import pbkdf2_sha256 as sha256
from app.models.user_model import User
from app.models.product_model import Product
from app.models.category_model import Category
from app.models.sale_model import Sale


class Database:

    def __init__(self, url=None):

        try:
            self.url = url
            parsed_url = urlparse(self.url)
            self.conn = psycopg2.connect(database=parsed_url.path[1:],
                                         user=parsed_url.username,
                                         password=parsed_url.password,
                                         host=parsed_url.hostname,
                                         port=parsed_url.port)

            self.cursor = self.conn.cursor()
            commands = (
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    date_created TIMESTAMPTZ DEFAULT NOW(),
                    is_admin BOOLEAN DEFAULT FALSE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS blacklist (
                    revoke_id SERIAL PRIMARY KEY,
                    code VARCHAR(255)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS categories (
                   category_id SERIAL PRIMARY KEY,
                   category_name VARCHAR(255) NOT NULL UNIQUE,
                   user_id INTEGER NOT NULL,
                   FOREIGN KEY (user_id)
                       REFERENCES users (user_id)
                       ON UPDATE CASCADE ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id SERIAL PRIMARY KEY,
                    product_name VARCHAR(255) NOT NULL UNIQUE,
                    quantity INTEGER NOT NULL,
                    price INTEGER NOT NULL,
                    date_added TIMESTAMPTZ DEFAULT NOW(),
                    category_id INTEGER NOT NULL,
                    FOREIGN KEY (category_id)
                    REFERENCES categories (category_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS sales (
                    sale_id INTEGER PRIMARY KEY NOT NULL,
                    sale_date TIMESTAMPTZ DEFAULT NOW(),
                    total INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS sold (
                    product_id INTEGER NOT NULL,
                    FOREIGN KEY (product_id)
                    REFERENCES products (product_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    sale_id INTEGER NOT NULL,
                    FOREIGN KEY (sale_id)
                    REFERENCES sales (sale_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    quantity INTEGER NOT NULL                   
                )
                """,
                """
                INSERT INTO users (name, username, password, is_admin) 
                SELECT * FROM (SELECT 'admin34', 'admin34', '{}', TRUE) 
                AS tmp WHERE NOT EXISTS (SELECT name FROM users WHERE username = 'admin34') LIMIT 1;
                """.format(sha256.hash('admin34'))
                )

            for command in commands:
                self.cursor.execute(command)
                self.conn.commit()
        except psycopg2.OperationalError as e:
            print('Unable to connect!\n{0}'.format(e))
            sys.exit(1)

    def drop_tables(self, table):
        """select an item by id in a respective table"""
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        cur.execute(f"DROP TABLE {table} CASCADE")

    # Queries for the user table
    def create_user(self, name, username, password):
        """Insert an item in a respective table"""
        query = f"INSERT INTO users(name, username, password)\
                            VALUES('{name}', '{username}', '{password}');"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def delete_user(self, user_id):
        """Insert an item in a respective table"""
        query = f"DELETE FROM users WHERE user_id = {user_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def find_user_by_username(self, username):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            user = User(result[0], result[1], result[2], result[3], result[4], result[5])
            return user

    def find_user_by_id(self, user_id):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM users WHERE user_id = {user_id}"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            user = User(result[0], result[1], result[2], result[3], result[4], result[5])
            return user

    def modify_admin_rights(self, user_id, status):
        """Insert an item in a respective table"""
        query = f"UPDATE  users SET is_admin = {status} WHERE user_id = {user_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def get_all_users(self):
        """select all users in users table"""
        query = f"SELECT * FROM users"
        cur = self.conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        if not results:
            return False
        users = []
        for result in results:
            user = User(result[0], result[1], result[2], result[3], result[4], result[5]).to_json()
            users.append(user)
        return users

    # Queries for the category table
    def add_category(self, category_name, user_id):
        """Insert an item in a respective table"""
        query = f"INSERT INTO categories(category_name, user_id) VALUES('{category_name}', {user_id});"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def modify_category(self, category_name, category_id):
        """Insert an item in a respective table"""
        query = f"UPDATE  categories SET category_name = '{category_name}' WHERE category_id = {category_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def delete_category(self, category_id):
        """Insert an item in a respective table"""
        query = f"DELETE FROM categories WHERE category_id = {category_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def find_category_by_category_name(self, category_name):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM categories WHERE category_name = '{category_name}'"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            category = Category(result[0], result[1], result[2])
            return category

    def find_category_by_category_id(self, category_name):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM categories WHERE category_id = {category_name}"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            category = Category(result[0], result[1], result[2])
            return category

    def get_all_categories(self):
        """select all category in categories table"""
        query = f"SELECT * FROM categories"
        cur = self.conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        if not results:
            return False
        categories = []
        for result in results:
            category = Category(result[0], result[1], result[2]).to_json()
            categories.append(category)
        return categories

    # Queries for the product table
    def add_product(self, product_name, quantity, price, user_id, category_id):
        """Insert an product in a respective products table"""
        query = f"INSERT INTO products(product_name, quantity, price, user_id, category_id) " \
                f"VALUES('{product_name}', {quantity}, {price}, {user_id}, {category_id});"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def modify_product(self, product_name, quantity, price, product_id):
        """Insert an item in a respective table"""
        query = f"UPDATE  products SET product_name = '{product_name}', quantity = {quantity}, price = {price}" \
                f"WHERE product_id = {product_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def update_stock(self, quantity, product_id):
        """Insert an item in a respective table"""
        query = f"UPDATE  products SET quantity = {quantity}" \
                f"WHERE product_id = {product_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def delete_product(self, product_id):
        """Insert an item in a respective table"""
        query = f"DELETE FROM products WHERE product_id = {product_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def find_product_by_product_name(self, product_name):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM products WHERE product_name = '{product_name}'"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            product = Product(result[0], result[1], result[2], result[3])
            return product

    def find_product_by_product_id(self, product_id):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM products WHERE product_id = {product_id}"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            product = Product(result[0], result[1], result[2], result[3])
            return product

    def get_all_products(self):
        """select all sales records in sales table"""
        query = f"SELECT * FROM products"
        cur = self.conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        if not results:
            return False
        products = []
        for result in results:
            product = Product(result[0], result[1], result[2], result[3]).to_json()
            products.append(product)
        return products

    # Queries for the sale table
    def add_sale(self, total, user_id, sale_id):
        """Insert an sale in a respective products table"""
        query = f"INSERT INTO sales(total, user_id, sale_id) " \
                f"VALUES('{total}', '{user_id}', '{sale_id}');"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def find_sale_by_sale_id(self, sale_id):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM sales WHERE sale_id = '{sale_id}'"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            sale = Sale(result[0], result[1], result[2], result[3])
            return sale

    def find_sale_by_user_id(self, user_id):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM sales WHERE user_id = {user_id}"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        if result:
            sale = Sale(result[0], result[1], result[2], result[3])
            return sale

    def get_all_sales(self):
        """select all sales records in sales table"""
        query = f"SELECT * FROM sales"
        cur = self.conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        sales = []
        if not results:
            return False
        for result in results:
            sale = Sale(result[0], result[1], result[2], result[3]).to_json()
            sales.append(sale)
        return sales

    # Queries for the sale table
    def add_sold_item(self, quantity, product_id, sale_id):
        """Insert an product in a respective products table"""
        query = f"INSERT INTO sold(quantity, product_id, sale_id) " \
                f"VALUES( {quantity}, {product_id}, {sale_id});"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def get_max_sale_id(self):
        """select all sales records in sales table"""
        query = "SELECT sale_id FROM sales;"
        cur = self.conn.cursor()
        cur.execute(query)
        results = cur.fetchall()
        sale_ids = []
        for result in results:
            sale_ids.append(result[0])
            print(results)
            print(sale_ids)
        return sale_ids

