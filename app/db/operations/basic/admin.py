from app import DB
from app.db.models.admin import Admin


class AdminOp:

    @classmethod
    def get(cls, id=None, name=None):

        filters = dict()
        if id:
            filters.update({"id": id})

        if name:
            filters.update({"name": name})

        result = Admin.query.filter_by(**filters).all()

        return result

    @classmethod
    def add(cls, name):
        new_admin = Admin(name)
        DB.session.add(new_admin)
        DB.session.commit()
        return new_admin

    @classmethod
    def update(cls, admin_obj, name):
        admin_obj.name = name

        DB.session.add(admin_obj)
        DB.session.commit()
        return admin_obj

    @classmethod
    def delete(cls, admin_obj):
        DB.session.delete(admin_obj)
        DB.session.commit()
