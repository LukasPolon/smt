from app import DB
from werkzeug.exceptions import NotFound

from app.db.models.server_tag import server_tag


class Tag(DB.Model):
    __tablename__ = "tag"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)

    servers = DB.relationship(
        "Server",
        secondary=server_tag,
        lazy="subquery",
        backref=DB.backref("tags", lazy=True),
    )

    def __init__(self, name):
        """ Constructor for Tag model."""
        self.name = name

    def __repr__(self):
        """ String representation of Tag model object."""
        return f"{self.name}"
