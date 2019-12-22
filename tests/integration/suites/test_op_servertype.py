from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.server_type import ServerType
from app.db.operations.basic.server_type import ServerTypeOp


@mark.db_operations
@mark.op_serverstatus
class TestServerTypeOp(Asserts):
    """ Integration tests for TestServerTypeOp class.
        Operations on ServerType model.
    """

    def case_add_records(self, refresh_db_before):
        """ Add new records to ServerType table."""
        new_types = ["Type one", "Type two"]

        for serv_type in new_types:
            ServerTypeOp.add(serv_type)

        check_records = ServerTypeOp.get()

        self.assertEqual(len(check_records), len(new_types))

        for record, exp_status in zip(check_records, new_types):
            self.assertTrue(isinstance(record, ServerType))
            self.assertEqual(record.name, exp_status)

    def case_get_by_id(self, refresh_db_before):
        """ Create test records in ServerType table and get them by id."""
        types_with_id = {"Type one": 1, "Type two": 2}

        for serv_type in types_with_id.keys():
            ServerTypeOp.add(serv_type)

        for exp_type, exp_id in types_with_id.items():
            type_obj = ServerTypeOp.get(id=exp_id)
            self.assertTrue(len(type_obj) is 1)
            self.assertEqual(exp_type, type_obj[0].name)
            self.assertEqual(exp_id, type_obj[0].id)

    def case_get_by_name_one_result(self, refresh_db_before):
        """ Create test records in ServerType table and get them by name."""
        types_with_id = {"Type one": 1, "Type two": 2}

        for serv_type in types_with_id.keys():
            ServerTypeOp.add(serv_type)

        for exp_type, exp_id in types_with_id.items():
            type_obj = ServerTypeOp.get(name=exp_type)
            self.assertTrue(len(type_obj) is 1)
            self.assertEqual(exp_type, type_obj[0].name)
            self.assertEqual(exp_id, type_obj[0].id)

    def case_update_record(self, refresh_db_before):
        """ Create test record in ServerType table and then update it."""
        original_type = "TypeOrig"
        update_type = "TypeUpdate"

        original_type_obj = ServerTypeOp.add(original_type)

        updated_type_local = ServerTypeOp.update(original_type_obj, update_type)

        self.assertEqual(updated_type_local.name, update_type)

        updated_type_get = ServerTypeOp.get(name=update_type)

        self.assertTrue(len(updated_type_get) is 1)
        self.assertEqual(updated_type_get[0].name, update_type)
        self.assertEqual(updated_type_get[0].id, original_type_obj.id)

    def case_delete_records(self, refresh_db_before):
        """ Create new record in ServerType table and then delete it."""
        new_type = "New type"

        ServerTypeOp.add(new_type)

        type_obj = ServerTypeOp.get(name=new_type)
        self.assertTrue(len(type_obj) is 1)
        self.assertEqual(type_obj[0].name, new_type)

        ServerTypeOp.delete(type_obj[0])

        type_obj = ServerTypeOp.get(name=new_type)
        self.assertFalse(type_obj)
