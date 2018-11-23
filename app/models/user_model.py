users = []


class User:
    """
        A class used to represent a Product

        ...

        Attributes
        ----------
        name : str
            the name of the user
        username : str
            the name of the user
        password : str
            the password of the user

        Methods
        -------
        to_json(self)
            Converts the product instance to a dictionary
    """
    def __init__(self, user_id, name, username, password, date, is_admin):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.date = date
        self.is_admin = is_admin

    def __repr__(self):
        """A method to returns the string representation of an object"""
        return f"User: {self.username} of ID {self.user_id} has successfully been added to the system"

    def to_json(self):
        """A method to Convert the product instance to a dictionary"""
        user = {
            'user_id': self.user_id,
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'is_admin': self.is_admin
        }
        return user

