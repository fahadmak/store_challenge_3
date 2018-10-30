categories = []


class Category:
    """
        A class used to represent a Category

        ...

        Attributes
        ----------
        category_id : int
            the name of the category
        category_name : str
            the name of the category
        user_id : int
            the quantity of the category

        Methods
        -------
        to_json(self)
            Converts the category instance to a dictionary
    """
    def __init__(self, category_id, category_name, user_id):
        self.category_id = category_id
        self.category_name = category_name
        self.user_id = user_id

    def __repr__(self):
        """A method to returns the string representation of an object"""
        return f"category: {self.category_name} of ID {self.category_id} has been added to inventory"

    def to_json(self):
        """A method to Convert the product instance to a dictionary"""
        category = {
            'categoryId': self.category_id,
            'name': self.category_name,
            'user_id': self.user_id,
        }
        return category
