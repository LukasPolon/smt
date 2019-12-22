from app import DB

from werkzeug.exceptions import NotFound

from app.db.models.server_status import ServerStatus
from app.db.models.server_type import ServerType


class Server(DB.Model):
    __tablename__ = "server"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)
    description = DB.Column(DB.String())
    status_id = DB.Column(DB.Integer, DB.ForeignKey("server_status.id"), nullable=False)
    type_id = DB.Column(DB.Integer, DB.ForeignKey("server_type.id"), nullable=False)

    def __init__(self, name, type_id, status_id, description):
        self.name = name
        self.type_id = type_id
        self.status_id = status_id
        if description:
            self.description = description

    def __repr__(self):
        return f"{self.name}"
