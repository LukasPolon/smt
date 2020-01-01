import re

from app import DB
from app.db.models.server_type import ServerType
from app.db.exceptions import ServerTypeIdNotValidError
from app.db.exceptions import ServerTypeNameNotValidError


class ServerTypeOp:
    """ Operations for ServerType model."""

    @classmethod
    def validate_id(cls, id):
        """ Field: id validation.

            Requirements:
                - must be integer

            Args:
                id(int): ServerType model id field
        """
        if not isinstance(id, int):
            raise ServerTypeIdNotValidError("Field: id must be Integer.")

    @classmethod
    def validate_name(cls, name):
        """ Field: name validation.

            Requirements:
                - must consist of at least 1 and maximum 20 characters
                - must consist of characters defined by regex: [A-Za-z ]+
                - must start with capital letter

            Args:
                name(str): ServerType model name field
        """
        if not isinstance(name, str):
            raise ServerTypeNameNotValidError("Field: name must be String.")

        if len(name) < 1 or len(name) > 20:
            raise ServerTypeNameNotValidError(
                "Field: name have wrong length. Should be in range 1 - 20."
            )

        if not re.match(r"[A-Za-z ]+\Z", name):
            raise ServerTypeNameNotValidError(
                "Field: name does not match regex: [A-Za-z ]+"
            )

        if not name[0].isupper():
            raise ServerTypeNameNotValidError(
                "Field: name must start with capital letter."
            )

    @classmethod
    def get(cls, id=None, name=None):
        """ Get ServerType rows filtered by parameters.

            Args:
                id(int): filter by id field
                name(str): filter by name field

            Return:
                result(list): list of row (ServerType) objects
        """
        filters = dict()
        if id:
            cls.validate_id(id)
            filters.update({"id": id})

        if name:
            cls.validate_name(name)
            filters.update({"name": name})

        result = ServerType.query.filter_by(**filters).all()

        return result

    @classmethod
    def add(cls, name):
        """ Add new ServerType row.

            Args:
                name(str): new ServerType row name field

            Returns:
                new_status(ServerType): ServerType row object
        """
        cls.validate_name(name)
        new_status = ServerType(name)
        DB.session.add(new_status)
        DB.session.commit()
        return new_status

    @classmethod
    def update(cls, type_obj, name):
        """ Update existing ServerType row.

            Args:
                type_obj(ServerType): current ServerType object
                name(str): new name field

            Returns:
                status_obj(ServerType): updated ServerType row object
        """
        cls.validate_name(name)
        type_obj.name = name
        DB.session.add(type_obj)
        DB.session.commit()
        return type_obj

    @classmethod
    def delete(cls, type_obj):
        """ Delete existing ServerType row.

            Args:
                type_obj(ServerType): existing ServerType row object
        """
        DB.session.delete(type_obj)
        DB.session.commit()
