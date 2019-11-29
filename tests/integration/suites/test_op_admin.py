from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.admin import Admin
from app.db.operations.basic.admin import AdminOp


@mark.db_operations
@mark.op_admin
class TestAdminOp(Asserts):
    """ Integration tests for AdminOp class.
        Operations on Admin model.
    """

    def case_add_records(self, refresh_db_before):
        """ Add new records to Admin table."""
        new_names = ["admin1", "admin2", "admin3"]

        for name in new_names:
            AdminOp.add(name)

        check_records = AdminOp.get()

        self.assertEqual(len(check_records), len(new_names))

        for record, exp_name in zip(check_records, new_names):
            self.assertTrue(isinstance(record, Admin))
            self.assertEqual(record.name, exp_name)

    def case_get_by_id(self, refresh_db_before):
        """ Create test records in Admin table and get them by id."""
        names_with_id = {"admin1": 1, "admin2": 2, "admin3": 3}

        for name in names_with_id.keys():
            AdminOp.add(name)

        for exp_name, exp_id in names_with_id.items():
            admin_obj = AdminOp.get(id=exp_id)
            self.assertTrue(len(admin_obj) is 1)
            self.assertEqual(exp_name, admin_obj[0].name)
            self.assertEqual(exp_id, admin_obj[0].id)

    def case_get_by_name_one_result(self, refresh_db_before):
        """ Create test records in Admin table and get them by name."""
        names_with_id = {"admin1": 1, "admin2": 2, "admin3": 3}

        for name in names_with_id.keys():
            AdminOp.add(name)

        for exp_name, exp_id in names_with_id.items():
            admin_obj = AdminOp.get(name=exp_name)
            self.assertTrue(len(admin_obj) is 1)
            self.assertEqual(exp_name, admin_obj[0].name)
            self.assertEqual(exp_id, admin_obj[0].id)

    def case_update_record(self, refresh_db_before):
        """ Create test record in Admin table and then update it."""
        original_name = "admin3"
        update_name = "admin33"

        original_admin = AdminOp.add(original_name)

        updated_admin_local = AdminOp.update(original_admin, update_name)

        self.assertEqual(updated_admin_local.name, update_name)

        updated_admin_get = AdminOp.get(name=update_name)

        self.assertTrue(len(updated_admin_get) is 1)
        self.assertEqual(updated_admin_get[0].name, update_name)
        self.assertEqual(updated_admin_get[0].id, original_admin.id)

    def case_delete_records(self, refresh_db_before):
        """ Create new record in Admin table and then delete it."""
        new_name = "admin1"

        AdminOp.add(new_name)

        adm_obj = AdminOp.get(name=new_name)
        self.assertTrue(len(adm_obj) is 1)
        self.assertEqual(adm_obj[0].name, new_name)

        AdminOp.delete(adm_obj[0])

        adm_obj = AdminOp.get(name=new_name)
        self.assertFalse(adm_obj)
