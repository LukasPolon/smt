from app import DB


class ServerType(DB.Model):
    __tablename__ = "server_type"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)
    servers = DB.relationship("Server", backref="type", lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name
