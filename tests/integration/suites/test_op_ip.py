from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.ip import Ip
from app.db.operations.basic.ip import IpOp


@mark.db_operations
@mark.op_ip
class TestIpOp(Asserts):

    """ Integration tests for IpOp class.
        Operations on Ip model.
    """

    def case_add_records(self, refresh_db_before):
        """ Add new records to Ip table."""
        new_addresses = ["0.0.0.0", "11.11.11.11", "222.222.222.222"]

        for address in new_addresses:
            IpOp.add(address)

        check_records = IpOp.get()

        self.assertEqual(len(check_records), len(new_addresses))

        for record, exp_name in zip(check_records, new_addresses):
            self.assertTrue(isinstance(record, Ip))
            self.assertEqual(record.address, exp_name)

    def case_get_by_id(self, refresh_db_before):
        """ Create test records in Ip table and get them by id."""
        addresses_with_id = {
            "0.0.0.0": 1,
            "11.11.11.11": 2,
            "222.222.222.222": 3,
        }

        for address in addresses_with_id.keys():
            IpOp.add(address)

        for exp_address, exp_id in addresses_with_id.items():
            ip_obj = IpOp.get(id=exp_id)
            self.assertTrue(len(ip_obj) is 1)
            self.assertEqual(exp_address, ip_obj[0].address)
            self.assertEqual(exp_id, ip_obj[0].id)

    def case_get_by_address_one_result(self, refresh_db_before):
        """ Create test records in Ip table and get them by name."""
        addresses_with_id = {
            "0.0.0.0": 1,
            "11.11.11.11": 2,
            "222.222.222.222": 3,
        }

        for address in addresses_with_id.keys():
            IpOp.add(address)

        for exp_address, exp_id in addresses_with_id.items():
            ip_obj = IpOp.get(address=exp_address)
            self.assertTrue(len(ip_obj) is 1)
            self.assertEqual(exp_address, ip_obj[0].address)
            self.assertEqual(exp_id, ip_obj[0].id)

    def case_update_record(self, refresh_db_before):
        """ Create test record in Ip table and then update it."""
        original_address = "0.0.0.0"
        update_address = "11.11.11.11"

        original_ip = IpOp.add(original_address)

        updated_ip_local = IpOp.update(original_ip, update_address)

        self.assertEqual(updated_ip_local.address, update_address)

        updated_ip_get = IpOp.get(address=update_address)

        self.assertTrue(len(updated_ip_get) is 1)
        self.assertEqual(updated_ip_get[0].address, update_address)
        self.assertEqual(updated_ip_get[0].id, original_ip.id)

    def case_delete_records(self, refresh_db_before):
        """ Create new record in Ip table and then delete it."""
        new_address = "0.0.0.0"

        IpOp.add(new_address)

        ip_obj = IpOp.get(address=new_address)
        self.assertTrue(len(ip_obj) is 1)
        self.assertEqual(ip_obj[0].address, new_address)

        IpOp.delete(ip_obj[0])

        ip_obj = IpOp.get(address=new_address)
        self.assertFalse(ip_obj)
