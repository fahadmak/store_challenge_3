sales = []
sale_ids = []


class Sale:
    """
        A class used to represent a Sale Record

        ...

        Attributes
        ----------
        sale_id : int
            the id of sale
        total : int
            total sale
        sale_date : str
            date and time of sale
        user_id : str
            id of sale attendant

        Methods
        -------
        to_json(self)
            Converts the sale record instance to a dictionary
    """
    def __init__(self, sale_id, total, sale_date, user_id):
        self.sale_id = sale_id
        self.user_id = user_id
        self.sale_date = sale_date
        self.total = total

    def __repr__(self):
        """A method to returns the string representation of an object"""
        return f"A sale of ID {self.sale_id} has successfully been added to the system on {self.sale_date}"

    def to_json(self):
        """A method to Convert the sale instance to a dictionary"""
        sale = {
            'user_id': self.user_id,
            'sale_id': self.sale_id,
            'sale_date': self.sale_date,
            'total': self.total
        }
        return sale


class Sold:
    """
        A class used to represent a Sold_Item

        ...

        Attributes
        ----------
        sale_id : int
            id of sale record
        product_name : str
            the name of the product
        quantity : int
            quantity of item sold
        product_id : int
            id of the product sold

        Methods
        -------
        to_json(self)
            Converts the sale record instance to a dictionary
    """
    def __init__(self, sale_id, product_name, quantity, product_id):
        self.sale_id = sale_id
        self.product_name = product_name
        self.quantity = quantity
        self.product_id = product_id

    def __repr__(self):
        """A method to returns the string representation of an object"""
        return f"{self.quantity} units {self.product_name} has been purchased"

    def to_json(self):
        """A method to Convert the sale instance to a dictionary"""
        item = {
            'product_id': self.product_id,
            'sale_id': self.sale_id,
            'quantity': self.quantity,
            'product_name': self.product_name
        }
        return item



