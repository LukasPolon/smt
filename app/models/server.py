from app import DB


class Server(DB.Model):
    __tablename__ = 'server'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String())
    description = DB.Column(DB.String())
    type_id = DB.Column(DB.Integer)
