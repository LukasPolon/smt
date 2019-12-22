import re

from app import DB
from app.db.models.server import Server
from app.db.operations.basic.server_status import ServerStatusOp
from app.db.operations.basic.server_type import ServerTypeOp


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
            raise ValueError("Field: id must be Integer.")

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
            raise ValueError("Field: name must be String.")

        if len(name) < 1 or len(name) > 30:
            raise ValueError("Field: name have wrong length. Should be in range 1-30.")

        if not re.match(r"[A-Za-z0-9_]+\Z", name):
            raise ValueError("Field: name does not match regex: [A-Za-z0-9_]+")

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
            raise ValueError("Field: description must be String.")

        if len(desc) < 1 or len(desc) > 60:
            raise ValueError(
                "Field: description have wrong length. Should be in range 1-60."
            )

        if not re.match(r"[A-Za-z0-9_ ]+\Z", desc):
            raise ValueError("Field: name does not match regex: [A-Za-z0-9_ ]+")

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
            raise ValueError(f'Not found status name: "{status_name}".')

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
            raise ValueError(f'Not found type name: "{type_name}".')

        type_id = type_results[0].id
        return type_id

    @classmethod
    def get(cls, id=None, name=None, srv_status=None, srv_type=None):
        """ Get Server rows filtered by parameters.

            Args:
                id(int): filter by id field
                name(str): filter by name field
                srv_status(str): filter by ServerStatus name
                srv_type(str): filter by ServerType name

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
        return result

    @classmethod
    def add(cls, name, srv_status, srv_type, description=None):
        """ Add new Server row.

            Args:
                name(str): server name
                srv_status(str): ServerStatus name
                srv_type(str): ServerType name
                description(str): Server description

            Returns:
                new_server(Server): server object
        """
        cls.validate_name(name)
        srv_status_id = cls.resolve_status(srv_status)
        srv_type_id = cls.resolve_type(srv_type)
        new_server = Server(name, srv_type_id, srv_status_id, description)
        DB.session.add(new_server)
        DB.session.commit()
        return new_server

    @classmethod
    def update(
        cls, server_obj, name=None, srv_status=None, srv_type=None, description=None
    ):
        """ Update existing Server row.

            Args:
                server_obj(Server): current Server object
                name(str): new name field
                srv_status(str): new server status name
                srv_type(str): new server type name
                description(str): new description field

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
