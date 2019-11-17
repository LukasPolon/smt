from app import DB
from werkzeug.exceptions import NotFound

from app.models.server_ip import server_ip


class Ip(DB.Model):
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
        self.address = address

    def __repr__(self):
        return self.address

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first_or_404(
            description=f"[SQL][{cls.__tablename__}] Not found ID: {id}."
        )

    @classmethod
    def get_by_address(cls, address):
        result = cls.query.filter_by(address=address).all()
        if not len(result):
            raise NotFound(
                description=f"[SQL][{cls.__tablename__}] Not found Address: {address}"
            )
