from app import DB


class Admin(DB.Model):
    """ Admin table model """

    __tablename__ = "admin"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False, unique=True)

    def __init__(self, name):
        """ Constructor for Admin model."""
        self.name = name

    def __repr__(self):
        """ String representation of Admin model object."""
        return f"{self.name}"
