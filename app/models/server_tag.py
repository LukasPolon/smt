from app import DB


server_tag = DB.Table(
    "server_tag",
    DB.Column("server_id", DB.Integer, DB.ForeignKey("server.id"), primary_key=True),
    DB.Column("tag_id", DB.Integer, DB.ForeignKey("tag.id"), primary_key=True),
)
