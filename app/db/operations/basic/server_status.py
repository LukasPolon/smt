import re

from app import DB
from app.db.models.server_status import ServerStatus
from app.db.exceptions import ServerStatusIdNotValidError
from app.db.exceptions import ServerStatusNameNotValidError


class ServerStatusOp:
    """ Operations for ServerStatus model."""

    @classmethod
    def validate_id(cls, id):
        """ Field: id validation.

            Requirements:
                - must be integer

            Args:
                id(int): ServerStatus model id field
        """
        if not isinstance(id, int):
            raise ServerStatusIdNotValidError("Field: id must be Integer.")

    @classmethod
    def validate_name(cls, name):
        """ Field: name validation.

            Requirements:
                - must consist of at least 1 and maximum 20 characters
                - must consist of characters defined by regex: [A-Za-z_]+
                - must start with capital letter

            Args:
                name(str): ServerStatus model name field
        """
        if not isinstance(name, str):
            raise ServerStatusNameNotValidError("Field: name must be String.")

        if len(name) < 1 or len(name) > 20:
            raise ServerStatusNameNotValidError(
                "Field: name have wrong length. Should be in range 1 - 20."
            )

        if not re.match(r"[A-Za-z_]+\Z", name):
            raise ServerStatusNameNotValidError(
                "Field: name does not match regex: [A-Za-z_]+"
            )

        if not name[0].isupper():
            raise ServerStatusNameNotValidError(
                "Field: name must start with capital letter."
            )

    @classmethod
    def get(cls, id=None, name=None):
        """ Get ServerStatus rows filtered by parameters.

            Args:
                id(int): filter by id field
                name(str): filter by name field

            Return:
                result(list): list of row (ServerStatus) objects
        """
        filters = dict()
        if id:
            cls.validate_id(id)
            filters.update({"id": id})

        if name:
            cls.validate_name(name)
            filters.update({"name": name})

        result = ServerStatus.query.filter_by(**filters).all()

        return result

    @classmethod
    def add(cls, name):
        """ Add new ServerStatus row.

            Args:
                name(str): new ServerStatus row name field

            Returns:
                new_status(ServerStatus): ServerStatus row object
        """
        cls.validate_name(name)
        new_status = ServerStatus(name)
        DB.session.add(new_status)
        DB.session.commit()
        return new_status

    @classmethod
    def update(cls, status_obj, name):
        """ Update existing ServerStatus row.

            Args:
                status_obj(ServerStatus): current ServerStatus object
                name(str): new name field

            Returns:
                status_obj(ServerStatus): updated ServerStatus row object
        """
        cls.validate_name(name)
        status_obj.name = name
        DB.session.add(status_obj)
        DB.session.commit()
        return status_obj

    @classmethod
    def delete(cls, status_obj):
        """ Delete existing ServerStatus row.

            Args:
                status_obj(ServerStatus): existing ServerStatus row object
        """
        DB.session.delete(status_obj)
        DB.session.commit()
