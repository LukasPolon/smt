from app import DB
from werkzeug.exceptions import NotFound

from app.models.server_admin import server_admin


class Admin(DB.Model):
    __tablename__ = 'admin'

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(), nullable=False)

    servers = DB.relationship(
        "Server",
        secondary=server_admin,
        lazy="subquery",
        backref=DB.backref("admins", lazy=True),
    )

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
