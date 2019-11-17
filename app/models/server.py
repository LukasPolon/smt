from app import DB

from werkzeug.exceptions import NotFound

from app.models.tag import Tag
from app.models.server_tag import server_tag
from app.models.server_ip import server_ip
from app.models.server_admin import server_admin


class Server(DB.Model):
    __tablename__ = "server"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)
    description = DB.Column(DB.String())
    status_id = DB.Column(DB.Integer, DB.ForeignKey("server_status.id"), nullable=False)
    type_id = DB.Column(DB.Integer, DB.ForeignKey("server_type.id"), nullable=False)

    tags = DB.relationship(
        "Tag",
        secondary=server_tag,
        lazy="subquery",
        backref=DB.backref("servers", lazy=True),
    )

    ips = DB.relationship(
        "Ip",
        secondary=server_ip,
        lazy="subquery",
        backref=DB.backref("servers", lazy=True),
    )

    admins = DB.relationship(
        "Admin",
        secondary=server_admin,
        lazy="subquery",
        backref=DB.backref("servers", lazy=True),
    )

    def __init__(self, name, type_id, description=str()):
        self.name = name
        self.type_id = type_id
        self.description = description

    def __repr__(self):
        return f"{self.name}"

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first_or_404(
            description=f"[SQL][{cls.__tablename__}] Not found ID: {id}."
        )

    @classmethod
    def get_by_name(cls, name):
        result = cls.query.filter_by(name=name).all()
        if not len(result):
            raise NotFound(
                description=f"[SQL][{cls.__tablename__}] Not found Name: {name}"
            )
