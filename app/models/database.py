import psycopg2
import sys
from urllib.parse import urlparse


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
                    password VARCHAR(255) NOT NULL
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
                    category_id INTEGER NOT NULL,
                    FOREIGN KEY (category_id)
                    REFERENCES categories (category_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (user_id)
                    REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
                )
                """
                )

            for command in commands:
                self.cursor.execute(command)
                self.conn.commit()
        except psycopg2.OperationalError as e:
            print('Unable to connect!\n{0}'.format(e))
            sys.exit(1)

    # Queries for the user table
    def create_user(self, name, username, password):
        """Insert an item in a respective table"""
        query = f"INSERT INTO users(name, username, password)\
                            VALUES('{name}', '{username}', '{password}');"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

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

    def delete_product(self, product_id):
        """Insert an item in a respective table"""
        query = f"DELETE FROM products WHERE product_id = {product_id};"
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def get_item(self, *args):
        """select an item by id in a respective table"""
        query = f"SELECT * FROM {args[0]} WHERE {args[1]} = '{args[2]}';"
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchone()
        return result

    def drop_tables(self, table):
        """select an item by id in a respective table"""
        cur = self.conn.cursor()
        cur.execute("ROLLBACK")
        cur.execute(f"DROP TABLE {table} CASCADE")

