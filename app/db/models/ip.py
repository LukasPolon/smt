from app import DB


class Ip(DB.Model):
    """ Ip table model """

    __tablename__ = "ip"

    id = DB.Column(DB.Integer, primary_key=True)
    address = DB.Column(DB.String(), nullable=False)

    def __init__(self, address):
        """ Constructor for Ip model."""
        self.address = address

    def __repr__(self):
        """ String representation of Ip model object."""
        return self.address
