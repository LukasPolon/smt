from app import APP

from app.db.models.server import Server

from app.db.models.server_type import ServerType
from app.db.models.ip import Ip
from app.db.models.admin import Admin
from app.db.models.tag import Tag


@APP.route("/")
def hello():
    return "Hello World!"


@APP.route("/server")
def server():
    result = Server.get_by_id(1)
    return str(result)


@APP.route("/server_type")
def server_type():
    result = ServerType.get_by_id(1)
    return str(result)


if __name__ == "__main__":
    APP.run()
