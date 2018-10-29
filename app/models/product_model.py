products = []


class Product:
    """
        A class used to represent a Product

        ...

        Attributes
        ----------
        name : str
            the name of the product
        quantity : int
            the quantity of the product
        price : int
            the price of the product

        Methods
        -------
        to_json(self)
            Converts the product instance to a dictionary
    """
    def __init__(self, product_id, product_name, quantity, price):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        """A method to returns the string representation of an object"""
        return f"Product: {self.product_name} of ID {self.product_id} has been added to inventory"

    def to_json(self):
        """A method to Convert the product instance to a dictionary"""
        product = {
            'productId': self.product_id,
            'name': self.product_name,
            'price': self.price,
            'quantity': self.quantity
        }
        return product
