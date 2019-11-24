from pytest import fixture

from app import DB


@fixture
def refresh_db_before():
    """ Drop and create all tables in database.
        Before test case run.
    """
    DB.session.remove()
    DB.drop_all()
    DB.create_all()
    yield refresh_db_before


@fixture
def refresh_db_after():
    """ Drop and create all tables in database.
        After test case run.
    """
    yield refresh_db_before
    DB.session.remove()
    DB.drop_all()
    DB.create_all()
