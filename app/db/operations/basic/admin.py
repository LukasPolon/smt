import re

from app import DB
from app.db.models.admin import Admin


class AdminOp:
    """ Operations for Admin model. """

    @classmethod
    def validate_id(cls, id):
        """ Field: id validation.

            Requirements:
                - must be integer

            Args:
                id(int): Admin model id field
        """
        if not isinstance(id, int):
            raise ValueError("Field: id must be Integer.")

    @classmethod
    def validate_name(cls, name):
        """ Field: name validation.

            Requirements:
                - must consist of at least 1 and maximum 20 characters
                - must consist of characters defined by regex: [A-Za-z0-9 ]+

            Args:
                name(str): Admin model name field
        """
        if not isinstance(name, str):
            raise ValueError("Field: name must be String.")

        if len(name) < 1 or len(name) > 20:
            raise ValueError(
                "Field: name have wrong length. Should be in range 1 - 20."
            )

        if not re.match(r"[A-Za-z0-9 ]+\Z", name):
            raise ValueError("Field: name does not match regex: [A-Za-z0-9 ]+")

    @classmethod
    def get(cls, id=None, name=None):
        """ Get Admin rows filtered by parameters.

            Args:
                id(int): filter by id field
                name(str): filter by name field

            Return:
                result(list): list of row (Admin) objects
        """
        filters = dict()
        if id:
            cls.validate_id(id)
            filters.update({"id": id})

        if name:
            cls.validate_name(name)
            filters.update({"name": name})

        result = Admin.query.filter_by(**filters).all()

        return result

    @classmethod
    def add(cls, name):
        """ Add new Admin row.

            Args:
                name(str): new Admin row name field

            Returns:
                new_admin(Admin): Admin row object
        """
        cls.validate_name(name)
        new_admin = Admin(name)
        DB.session.add(new_admin)
        DB.session.commit()
        return new_admin

    @classmethod
    def update(cls, admin_obj, name):
        """ Update existing Admin row.

            Args:
                admin_obj(Admin): current Admin object
                name(str): new name field

            Returns:
                admin_obj(Admin): updated Admin row object
        """
        cls.validate_name(name)
        admin_obj.name = name
        DB.session.add(admin_obj)
        DB.session.commit()
        return admin_obj

    @classmethod
    def delete(cls, admin_obj):
        """ Delete existing Admin row.

            Args:
                admin_obj(Admin): existing Admin row object
        """
        DB.session.delete(admin_obj)
        DB.session.commit()
