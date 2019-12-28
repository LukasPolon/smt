from app import DB

from app.db.models.server_status import ServerStatus
from app.db.models.server_type import ServerType


server_ip = DB.Table(
    "server_ip",
    DB.Column("server_id", DB.Integer, DB.ForeignKey("server.id"), primary_key=True),
    DB.Column("ip_id", DB.Integer, DB.ForeignKey("ip.id"), primary_key=True),
)


server_tag = DB.Table(
    "server_tag",
    DB.Column("server_id", DB.Integer, DB.ForeignKey("server.id"), primary_key=True),
    DB.Column("tag_id", DB.Integer, DB.ForeignKey("tag.id"), primary_key=True),
)


server_admin = DB.Table(
    "server_admin",
    DB.Column("server_id", DB.Integer, DB.ForeignKey("server.id"), primary_key=True),
    DB.Column("admin_id", DB.Integer, DB.ForeignKey("admin.id"), primary_key=True),
)


class Server(DB.Model):
    """ Server table model. """

    __tablename__ = "server"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)
    description = DB.Column(DB.String())

    status_id = DB.Column(DB.Integer, DB.ForeignKey("server_status.id"), nullable=False)
    type_id = DB.Column(DB.Integer, DB.ForeignKey("server_type.id"), nullable=False)

    ips = DB.relationship(
        "Ip",
        secondary=server_ip,
        lazy="subquery",
        backref=DB.backref("servers", lazy=True),
    )

    tags = DB.relationship(
        "Tag",
        secondary=server_tag,
        lazy="subquery",
        backref=DB.backref("servers", lazy=True),
    )

    admins = DB.relationship(
        "Admin",
        secondary=server_admin,
        lazy="subquery",
        backref=DB.backref("servers", lazy=True),
    )

    def __init__(self, name, type_id, status_id, description=None, ips=None, tags=None):
        self.name = name
        self.type_id = type_id
        self.status_id = status_id
        if description:
            self.description = description
        if ips:
            self.ips = ips
        if tags:
            self.tags = tags

    def __repr__(self):
        return f"{self.name}"
