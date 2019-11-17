from app import APP

from app.models.server import Server
from app.models.server_type import ServerType
from app.models.server_status import ServerStatus
from app.models.ip import Ip
from app.models.tag import Tag
from app.models.admin import Admin


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
