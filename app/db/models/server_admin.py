from app import DB


server_admin = DB.Table(
    "server_admin",
    DB.Column("server_id", DB.Integer, DB.ForeignKey("server.id"), primary_key=True),
    DB.Column("admin_id", DB.Integer, DB.ForeignKey("admin.id"), primary_key=True),
)
