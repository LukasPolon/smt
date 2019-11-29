import re

from app import DB
from app.db.models.ip import Ip


class IpOp:
    """ Operations for Ip model. """

    @classmethod
    def validate_id(cls, id):
        """ Field: id validation.

            Requirements:
                - must be integer

            Args:
                id(int): Ip model id field
        """
        if not isinstance(id, int):
            raise ValueError("Field: id must be Integer.")

    @classmethod
    def validate_address(cls, address):
        """ Field: address validation.

            Requirements:
                - must consist of characters defined by regex:
                  \d{1,3}.\d{1,3}.\d{1,3}

            Args:
                address(str): Admin model name field
        """
        if not isinstance(address, str):
            raise ValueError("Field: address must be String.")

        if not re.match(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\Z", address):
            raise ValueError(
                "Field: name does not match regex: " "\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}"
            )

    @classmethod
    def get(cls, id=None, address=None):
        """ Get Ip rows filtered by parameters.

            Args:
                id(int): filter by id field
                address(str): filter by address field

            Return:
                result(list): list of row (Ip) objects
        """
        filters = dict()
        if id:
            cls.validate_id(id)
            filters.update({"id": id})

        if address:
            cls.validate_address(address)
            filters.update({"address": address})

        result = Ip.query.filter_by(**filters).all()

        return result

    @classmethod
    def add(cls, address):
        """ Add new Ip row.

            Args:
                address(str): new Ip row address field

            Returns:
                new_ip(Admin): Ip row object
        """
        cls.validate_address(address)
        new_ip = Ip(address)
        DB.session.add(new_ip)
        DB.session.commit()
        return new_ip

    @classmethod
    def update(cls, ip_obj, address):
        """ Update existing Ip row.

            Args:
                ip_obj(Ip): current Ip object
                address(str): new address field

            Returns:
                ip_obj(Ip): updated Ip row object
        """
        cls.validate_address(address)
        ip_obj.address = address
        DB.session.add(ip_obj)
        DB.session.commit()
        return ip_obj

    @classmethod
    def delete(cls, ip_obj):
        """ Delete existing Ip row.

            Args:
                ip_obj(Ip): existing Ip row object
        """
        DB.session.delete(ip_obj)
        DB.session.commit()


if __name__ == "__main__":

    fo = IpOp.get(id=2)
    IpOp.delete(fo[0])

    for i in IpOp.get():
        print(i.id, i.address)
