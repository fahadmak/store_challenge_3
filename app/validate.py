def validate(name, price, quantity):
    """A method to Check if name and price are of the correct form"""
    errors = {}
    if not isinstance(name, str):
        errors['name'] = "incorrect username format"
    if not isinstance(price, int):
        errors['price'] = "incorrect price format"
    if not isinstance(quantity, int):
        errors['quantity'] = "incorrect quantity format"
    return errors


def empty(name, price, quantity):
    """A method to Check if name and price are of the correct form"""
    errors = {}
    if not name:
        errors['name'] = "empty name field"
    if not price:
        errors['price'] = "empty price field"
    if not quantity:
        errors['quantity'] = "empty quantity field"
    return errors

def validate_user(name, username, password):
    """A method to Check if name and price are of the correct form"""
    errors = {}
    if not isinstance(name, str):
        errors['name'] = "incorrect name format"
    if not isinstance(username, str):
        errors['username'] = "incorrect username format"
    if not isinstance(password, str):
        errors['password'] = "incorrect password format"
    return errors
