""" Custom Database operations exceptions."""


class DbError(Exception):
    """ General custom database operations exception."""

    pass


# Admin model exceptions


class AdminError(DbError):
    """ Custom database operations exception for use
        in Admin model operations.
    """

    pass


class AdminIdNotValidError(AdminError):
    """ Exception for use in case of invalid ID parameter
        in Admin model operations.
    """

    pass


class AdminNameNotValidError(AdminError):
    """ Exception for use in case of invalid Name parameter
        in Admin model operations.
    """

    pass


# Ip model exceptions


class IpError(DbError):
    """ Custom database operations exception for use
        in Ip model operations.
    """

    pass


class IpIdNotValidError(IpError):
    """ Exception for use in case of invalid Name parameter
        in Ip model operations.
    """

    pass


class IpAddressNotValidError(IpError):
    """ Exception for use in case of invalid Address parameter
        in Ip model operations.
    """

    pass


class ServerStatusError(DbError):
    """ Custom database operations exception for use
        in ServerStatus model operations.
    """

    pass


# ServerStatus model exceptions


class ServerStatusIdNotValidError(ServerStatusError):
    """ Exception for use in case of invalid Id parameter
        in ServerStatus model operations.
    """

    pass


class ServerStatusNameNotValidError(ServerStatusError):
    """ Exception for use in case of invalid Name parameter
        in ServerStatus model operations.
    """

    pass


# ServerType model exceptions


class ServerTypeError(DbError):
    """ Custom database operations exception for use
        in ServerType model operations.
    """

    pass


class ServerTypeIdNotValidError(ServerTypeError):
    """ Exception for use in case of invalid Id parameter
        in ServerType model operations.
    """

    pass


class ServerTypeNameNotValidError(ServerTypeError):
    """ Exception for use in case of invalid Name parameter
        in ServerType model operations.
    """

    pass


# Tag model exceptions


class TagError(DbError):
    """ Custom database operations exception for use
        in Tag model operations.
    """

    pass


class TagIdNotValidError(TagError):
    """ Exception for use in case of invalid Id parameter
        in Tag model operations.
    """

    pass


class TagNameNotValidError(TagError):
    """ Exception for use in case of invalid Name parameter
        in Tag model operations.
    """

    pass


# Server model exceptions


class ServerError(DbError):
    """ Custom database operations exception for use
        in Server model operations.
    """

    pass


class ServerIdNotValidError(ServerError):
    """ Exception for use in case of invalid Id parameter
        in Server model operations.
    """

    pass


class ServerNameNotValidError(ServerError):
    """ Exception for use in case of invalid Name parameter
        in Server model operations.
    """

    pass


class ServerDescriptionNotValidError(ServerError):
    """ Exception for use in case of invalid Description parameter
        in Server model operations.
    """

    pass


class ServerStatusNotFoundError(ServerError):
    """ Exception for use in case if ServerStatus not found
        during resolving parameter.
    """

    pass


class ServerTypeNotFoundError(ServerError):
    """ Exception for use in case if ServerType not found
        during resolving parameter.
    """

    pass


class ServerIpNotFoundError(ServerError):
    """ Exception for use in case if Ip not found
        during resolving parameter.
    """

    pass


class ServerTagNotFoundError(ServerError):
    """ Exception for use in case if Tag not found
        during resolving parameter.
    """

    pass


class ServerAdminNotFoundError(ServerError):
    """ Exception for use in case if Admin not found
        during resolving parameter.
    """

    pass
