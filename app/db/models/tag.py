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
