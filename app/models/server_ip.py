from app import DB


server_ip = DB.Table(
    "server_ip",
    DB.Column("server_id", DB.Integer, DB.ForeignKey("server.id"), primary_key=True),
    DB.Column("ip_id", DB.Integer, DB.ForeignKey("ip.id"), primary_key=True),
)
