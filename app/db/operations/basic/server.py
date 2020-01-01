import re

from app import DB
from app.db.models.server import Server
from app.db.operations.basic.server_status import ServerStatusOp
from app.db.operations.basic.server_type import ServerTypeOp
from app.db.operations.basic.ip import IpOp
from app.db.operations.basic.tag import TagOp
from app.db.operations.basic.admin import AdminOp

from app.db.exceptions import ServerStatusError
from app.db.exceptions import ServerTypeError
from app.db.exceptions import IpError
from app.db.exceptions import TagError
from app.db.exceptions import AdminError

from app.db.exceptions import ServerIdNotValidError
from app.db.exceptions import ServerNameNotValidError
from app.db.exceptions import ServerDescriptionNotValidError
from app.db.exceptions import ServerStatusNotFoundError
from app.db.exceptions import ServerTypeNotFoundError
from app.db.exceptions import ServerIpNotFoundError
from app.db.exceptions import ServerTagNotFoundError
from app.db.exceptions import ServerAdminNotFoundError


class ServerOp:
    """ Operations for Server model."""

    @classmethod
    def validate_id(cls, id):
        """ Field: id validation.

            Requirements:
                - must be integer

            Args:
                id(int): Server model id field
        """
        if not isinstance(id, int):
            raise ServerIdNotValidError("Field: id must be Integer.")

    @classmethod
    def validate_name(cls, name):
        """ Field: name validation.

            Requirements:
                - must consist of at least 1 and maximum 30 characters
                - must consist of characters defined by regex: [A-Za-z0-9_]+

            Args:
                name(str): Server model name field
        """
        if not isinstance(name, str):
            raise ServerNameNotValidError("Field: name must be String.")

        if len(name) < 1 or len(name) > 30:
            raise ServerNameNotValidError(
                "Field: name have wrong length. Should be in range 1-30."
            )

        if not re.match(r"[A-Za-z0-9_]+\Z", name):
            raise ServerNameNotValidError(
                "Field: name does not match regex: [A-Za-z0-9_]+"
            )

    @classmethod
    def validate_description(cls, desc):
        """ Field: name validation.

            Requirements:
                - must consist of at least 1 and maximum 60 characters
                - must consist of characters defined by regex: [A-Za-z0-9_ ]+

            Args:
                desc(str): Server model description field
        """
        if not isinstance(desc, str):
            raise ServerDescriptionNotValidError("Field: description must be String.")

        if len(desc) < 1 or len(desc) > 60:
            raise ServerDescriptionNotValidError(
                "Field: description have wrong length. Should be in range 1-60."
            )

        if not re.match(r"[A-Za-z0-9_ ]+\Z", desc):
            raise ServerDescriptionNotValidError(
                "Field: name does not match regex: [A-Za-z0-9_ ]+"
            )

    @classmethod
    def resolve_status(cls, status_name):
        """ Find ServerStatus record according to given name.
            Return ID of status row.

            Args:
                status_name(str): ServerStatus record name

            Returns:
                status_id(int): ServerStatus record ID
        """
        status_results = ServerStatusOp.get(name=status_name)

        if len(status_results) is not 1:
            raise ServerStatusNotFoundError(f'Not found status name: "{status_name}".')

        status_id = status_results[0].id
        return status_id

    @classmethod
    def resolve_type(cls, type_name):
        """ Find ServerType record according to given name.
            Return ID of type row.

            Args:
                type_name(str): ServerType record name

            Returns:
                type_id(int): ServerType record ID
        """
        type_results = ServerTypeOp.get(name=type_name)

        if len(type_results) is not 1:
            raise ServerTypeNotFoundError(f'Not found type name: "{type_name}".')

        type_id = type_results[0].id
        return type_id

    @classmethod
    def resolve_ip(cls, ip_address):
        """ Find Ip record according to given address.
            Return Ip model object.

            Args:
                ip_address(str): address to find

            Returns:
                ip_obj(app.db.models.ip.Ip): Ip object
        """
        ip_results = IpOp.get(address=ip_address)

        if len(ip_results) is not 1:
            raise ServerIpNotFoundError(f"Not found IP address: {ip_address}.")

        ip_obj = ip_results[0]
        return ip_obj

    @classmethod
    def resolve_tag(cls, tag_name):
        """ Find Tag record according to given address.
            Return Tag model object.

            Args:
                tag_name(str): tag to find

            Returns:
                tag_obj(app.db.models.tag.Tag): Tag object
        """
        tag_results = TagOp.get(name=tag_name)

        if len(tag_results) is not 1:
            raise ServerTagNotFoundError(f"Not found Tag: {tag_name}.")

        tag_obj = tag_results[0]
        return tag_obj

    @classmethod
    def resolve_admin(cls, admin_name):
        """ Find Admin record according to given name.
            Return Admin model object.

            Args:
                admin_name(str): name to find

            Returns:
                admin_obj(app.db.models.admin.Admin): admin object
        """
        admin_results = AdminOp.get(name=admin_name)

        if len(admin_results) is not 1:
            raise ServerAdminNotFoundError(f"Not found Admin: {admin_name}.")

        admin_obj = admin_results[0]
        return admin_obj

    @classmethod
    def get(
        cls,
        id=None,
        name=None,
        srv_status=None,
        srv_type=None,
        ip=None,
        tags=None,
        admins=None,
    ):
        """ Get Server rows filtered by parameters.

            Args:
                id(int): filter by id field
                name(str): filter by name field
                srv_status(str): filter by ServerStatus name
                srv_type(str): filter by ServerType name
                ip(str): filter by Ip address
                tags(list): filter by list of tags
                admins(list): filter by list of admins names

            Returns:
                result(list): list of row (Server) objects
        """
        filters = dict()
        if id:
            cls.validate_id(id)
            filters.update({"id": id})
        if name:
            cls.validate_name(name)
            filters.update({"name": name})
        if srv_status:
            srv_status_id = cls.resolve_status(srv_status)
            filters.update({"status_id": srv_status_id})
        if srv_type:
            srv_type_id = cls.resolve_type(srv_type)
            filters.update({"type_id": srv_type_id})

        result = Server.query.filter_by(**filters).all()

        if ip:
            ip_obj = cls.resolve_ip(ip)
            result = [srv for srv in result if ip_obj in srv.ips]

        if tags:
            for tag in tags:
                tag_obj = cls.resolve_tag(tag)
                result = [srv for srv in result if tag_obj in srv.tags]

        if admins:
            for admin in admins:
                adm_obj = cls.resolve_admin(admin)
                result = [srv for srv in result if adm_obj in srv.admins]

        return result

    @classmethod
    def add(
        cls,
        name,
        srv_status,
        srv_type,
        description=None,
        ips=None,
        tags=None,
        admins=None,
    ):
        """ Add new Server row.

            Args:
                name(str): server name
                srv_status(str): ServerStatus name
                srv_type(str): ServerType name
                description(str): Server description
                ips(list): list of ip addresses (str) bounded to the server
                tags(list): list of tags names (str) bounded to the server
                admins(list): list of admin names (str) bounded to the server

            Returns:
                new_server(Server): server object
        """
        cls.validate_name(name)
        srv_status_id = cls.resolve_status(srv_status)
        srv_type_id = cls.resolve_type(srv_type)
        new_server = Server(name, srv_type_id, srv_status_id, description)
        if ips:
            new_server.ips = [cls.resolve_ip(ip) for ip in ips]
        if tags:
            new_server.tags = [cls.resolve_tag(tag) for tag in tags]
        if admins:
            new_server.admins = [cls.resolve_admin(admin) for admin in admins]
        DB.session.add(new_server)
        DB.session.commit()
        return new_server

    @classmethod
    def update(
        cls,
        server_obj,
        name=None,
        srv_status=None,
        srv_type=None,
        description=None,
        ips=None,
        tags=None,
        admins=None,
    ):
        """ Update existing Server row.

            Args:
                server_obj(Server): current Server object
                name(str): new name field
                srv_status(str): new server status name
                srv_type(str): new server type name
                description(str): new description field
                ips(list): new list of ip addresses (str) bounded to the server
                tags(list): new list of tags names (str) bounded to the server
                admins(list): new list of admin names (str) bounded to the server

            Returns:
                server_obj(Server): updated Server object
        """
        if name:
            cls.validate_name(name)
            server_obj.name = name
        if srv_status:
            srv_status_id = cls.resolve_status(srv_status)
            server_obj.status_id = srv_status_id
        if srv_type:
            srv_type_id = cls.resolve_type(srv_type)
            server_obj.type_id = srv_type_id
        if description:
            cls.validate_description(description)
            server_obj.description = description
        if ips:
            server_obj.ips = [cls.resolve_ip(ip) for ip in ips]
        if tags:
            server_obj.tags = [cls.resolve_tag(tag) for tag in tags]
        if admins:
            server_obj.admins = [cls.resolve_admin(admin) for admin in admins]

        DB.session.add(server_obj)
        DB.session.commit()
        return server_obj

    @classmethod
    def delete(cls, server_obj):
        """ Delete existing Server row.

            Args:
                server_obj(Server): existing Server row object
        """
        DB.session.delete(server_obj)
        DB.session.commit()
