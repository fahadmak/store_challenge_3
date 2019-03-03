import string

letters = tuple(string.ascii_letters)

user_schema = {'name': {'required': True, 'min': 6, 'type': 'string'},
               'username': {'type': 'string', 'min': 7, 'required': True},
               'password': {'type': 'string', 'min': 7,'required': True}}

login_schema = {'username': {'type': 'string', 'min': 7, 'required': True},
                'password': {'type': 'string', 'min': 7, 'required': True}}

product_schema = {'name': {'type': 'string', 'required': True, 'regex': '^[A-Za-z0-9]+$'},
                  'quantity': {'type': 'number', 'min': 1, 'required': True, 'forbidden': [' ', ""]},
                  'price': {'type': 'number', 'min': 1, 'required': True, 'forbidden': [' ', ""]}}

add_product_schema = {'name': {'type': 'string', 'required': True, 'regex': '^[A-Za-z0-9]+$'},
                      'quantity': {'type': 'integer', 'required': True, 'forbidden': [' ', "", "    "]},
                      'price': {'type': 'integer', 'required': True, 'forbidden': [' ', "", "    "]},
                      'category_id': {'type': 'integer', 'required': True, 'forbidden': [' ', "", "    "]}}

category_schema = {'category_name': {'type': 'string', 'required': True, 'forbidden': [' ', "", "    "]}}

sale_schema = {'quantity': {'type': 'integer', 'required': True, 'empty': True},
               'product_id': {'type': 'integer', 'required': True, 'empty': True}}
