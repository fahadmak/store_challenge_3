import string

letters = tuple(string.ascii_letters)

user_schema = {'name': {'required': True, 'min': 6, 'type': 'string', 'forbidden': [' ', "", "    "]},
               'username': {'type': 'string', 'min': 7, 'required': True, 'forbidden': [' ', "", "    "]},
               'password': {'type': 'string', 'required': True, 'forbidden': [' ', "", "    "]}}

login_schema = {'username': {'type': 'string', 'min': 7, 'required': True, 'forbidden': [' ', "", "      "]},
                'password': {'type': 'string', 'required': True, 'forbidden': [' ', "", "    "]}}

product_schema = {'product_name': {'type': 'string', 'required': True, 'forbidden': [' ', "", "   "]},
                  'quantity': {'type': 'integer', 'required': True, 'forbidden': [' ', ""]},
                  'product_price': {'type': 'integer', 'required': True, 'forbidden': [' ', ""]}}

add_product_schema = {'product_name': {'type': 'string', 'required': True, 'forbidden': [' ', "", "    "]},
                      'quantity': {'type': 'integer', 'required': True, 'forbidden': [' ', "", "    "]},
                      'product_price': {'type': 'integer', 'required': True, 'forbidden': [' ', "", "    "]},
                      'category_id': {'type': 'integer', 'required': True, 'forbidden': [' ', "", "    "]}}

category_schema = {'category_name': {'type': 'string', 'required': True, 'forbidden': [' ', "", "    "]}}

sale_schema = {'quantity': {'type': 'integer', 'required': True, 'empty': True},
               'product_id': {'type': 'integer', 'required': True, 'empty': True}}
