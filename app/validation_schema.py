
user_schema = {'name': {'required': True, 'min': 6, 'type': 'string'},
               'username': {'type': 'string', 'min': 7, 'required': True},
               'password': {'type': 'string', 'required': True}}

login_schema = {'username': {'type': 'string', 'min': 7, 'required': True},
                'password': {'type': 'string', 'required': True}}

product_schema = {'product_name': {'type': 'integer', 'required': True},
                  'quantity': {'type': 'integer', 'required': True},
                  'price': {'type': 'integer', 'required': True}}

category_schema = {'category_name': {'type': 'string', 'required': True}}

sale_schema = {'quantity': {'type': 'integer', 'required': True},
               'product_id': {'type': 'integer', 'required': True}}
