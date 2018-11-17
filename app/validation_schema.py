import string

letters = tuple(string.ascii_letters)

user_schema = {'name': {'required': True, 'min': 6, 'type': 'string', 'regex': '^[A-Za-z0-9]+$'},
               'username': {'type': 'string', 'min': 7, 'required': True, 'regex': '^[a-z0-9]{5,15}$'},
               'password': {'type': 'string', 'required': True, 'regex': '^[a-z0-9]{5,15}$'}}

login_schema = {'username': {'type': 'string', 'required': True, 'regex': '^[a-z0-9_@]{5,15}$'},
                'password': {'type': 'string', 'required': True, 'regex': '^[a-z0-9_@]{5,15}$'}}

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
