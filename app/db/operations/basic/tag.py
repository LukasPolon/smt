import re

from app import DB
from app.db.models.tag import Tag
from app.db.exceptions import TagIdNotValidError
from app.db.exceptions import TagNameNotValidError


class TagOp:
    """ Operations for Tag model. """

    @classmethod
    def validate_id(cls, id):
        """ Field: id validation.

            Requirements:
                - must be integer

            Args:
                id(int): Admin model id field
        """
        if not isinstance(id, int):
            raise TagIdNotValidError("Field: id must be Integer.")

    @classmethod
    def validate_name(cls, name):
        """ Field: name validation.

            Requirements:
                - must consist of at least 1 and maximum 15 characters
                - must consist of characters defined by regex: [A-Za-z0-9_ ]+

            Args:
                name(str): Admin model name field
        """
        if not isinstance(name, str):
            raise TagNameNotValidError("Field: name must be String.")

        if len(name) < 1 or len(name) > 15:
            raise TagNameNotValidError(
                "Field: name have wrong length. Should be in range 1 - 15."
            )

        if not re.match(r"[A-Za-z0-9_ ]+\Z", name):
            raise TagNameNotValidError(
                "Field: name does not match regex: [A-Za-z0-9_ ]+"
            )

    @classmethod
    def get(cls, id=None, name=None):
        """ Get Tag rows filtered by parameters.

            Args:
                id(int): filter by id field
                name(str): filter by name field

            Return:
                result(list): list of row (Tag) objects
        """
        filters = dict()
        if id:
            cls.validate_id(id)
            filters.update({"id": id})

        if name:
            cls.validate_name(name)
            filters.update({"name": name})

        result = Tag.query.filter_by(**filters).all()
        return result

    @classmethod
    def add(cls, name):
        """ Add new Tag row.

            Args:
                name(str): new Tag row name field

            Returns:
                new_tag(Tag): Tag row object
        """
        cls.validate_name(name)
        new_tag = Tag(name)
        DB.session.add(new_tag)
        DB.session.commit()
        return new_tag

    @classmethod
    def update(cls, tag_obj, name):
        """ Update existing Tag row.

            Args:
                tag_obj(Tag): current Tag object
                name(str): new name field

            Returns:
                tag_obj(Tag): updated Tag row object
        """
        cls.validate_name(name)
        tag_obj.name = name
        DB.session.add(tag_obj)
        DB.session.commit()
        return tag_obj

    @classmethod
    def delete(cls, tag_obj):
        """ Delete existing Tag row.

            Args:
                tag_obj(Tag): existing Tag row object
        """
        DB.session.delete(tag_obj)
        DB.session.commit()
