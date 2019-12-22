from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.server_status import ServerStatus
from app.db.operations.basic.server_status import ServerStatusOp


@mark.db_operations
@mark.op_serverstatus
class TestServerStatusOp(Asserts):
    """ Integration tests for ServerStatusOp class.
        Operations on ServerStatus model.
    """

    def case_add_records(self, refresh_db_before):
        """ Add new records to ServerStatus table."""
        new_statuses = ["Status_one", "Status_two"]

        for status in new_statuses:
            ServerStatusOp.add(status)

        check_records = ServerStatusOp.get()

        self.assertEqual(len(check_records), len(new_statuses))

        for record, exp_status in zip(check_records, new_statuses):
            self.assertTrue(isinstance(record, ServerStatus))
            self.assertEqual(record.name, exp_status)

    def case_get_by_id(self, refresh_db_before):
        """ Create test records in ServerStatus table and get them by id."""
        statuses_with_id = {"Status_one": 1, "Status_two": 2}

        for status in statuses_with_id.keys():
            ServerStatusOp.add(status)

        for exp_status, exp_id in statuses_with_id.items():
            stat_obj = ServerStatusOp.get(id=exp_id)
            self.assertTrue(len(stat_obj) is 1)
            self.assertEqual(exp_status, stat_obj[0].name)
            self.assertEqual(exp_id, stat_obj[0].id)

    def case_get_by_name_one_result(self, refresh_db_before):
        """ Create test records in ServerStatus table and get them by name."""
        statuses_with_id = {"Status_one": 1, "Status_two": 2}

        for status in statuses_with_id.keys():
            ServerStatusOp.add(status)

        for exp_status, exp_id in statuses_with_id.items():
            stat_obj = ServerStatusOp.get(name=exp_status)
            self.assertTrue(len(stat_obj) is 1)
            self.assertEqual(exp_status, stat_obj[0].name)
            self.assertEqual(exp_id, stat_obj[0].id)

    def case_update_record(self, refresh_db_before):
        """ Create test record in ServerStatus table and then update it."""
        original_status = "StatusOrig"
        update_status = "StatusUpdate"

        original_stat_obj = ServerStatusOp.add(original_status)

        updated_stat_local = ServerStatusOp.update(original_stat_obj, update_status)

        self.assertEqual(updated_stat_local.name, update_status)

        updated_stat_get = ServerStatusOp.get(name=update_status)

        self.assertTrue(len(updated_stat_get) is 1)
        self.assertEqual(updated_stat_get[0].name, update_status)
        self.assertEqual(updated_stat_get[0].id, original_stat_obj.id)

    def case_delete_records(self, refresh_db_before):
        """ Create new record in ServerStatus table and then delete it."""
        new_status = "NewStatus"

        ServerStatusOp.add(new_status)

        status_obj = ServerStatusOp.get(name=new_status)
        self.assertTrue(len(status_obj) is 1)
        self.assertEqual(status_obj[0].name, new_status)

        ServerStatusOp.delete(status_obj[0])

        status_obj = ServerStatusOp.get(name=new_status)
        self.assertFalse(status_obj)
