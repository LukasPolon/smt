from app import DB
from werkzeug.exceptions import NotFound


class ServerStatus(DB.Model):
    __tablename__ = "server_status"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)

    servers = DB.relationship("Server", backref="status", lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
