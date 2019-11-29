from app import DB

from app.db.models.server_ip import server_ip


class Ip(DB.Model):
    """ Ip table model """

    __tablename__ = "ip"

    id = DB.Column(DB.Integer, primary_key=True)
    address = DB.Column(DB.String(), nullable=False)

    servers = DB.relationship(
        "Server",
        secondary=server_ip,
        lazy="subquery",
        backref=DB.backref("ips", lazy=True),
    )

    def __init__(self, address):
        """ Constructor for Ip model."""
        self.address = address

    def __repr__(self):
        """ String representation of Ip model object."""
        return self.address
