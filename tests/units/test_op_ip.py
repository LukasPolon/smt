from unittest import TestCase
from unittest import mock

from app.db.operations.basic.ip import IpOp
from app.db.exceptions import IpIdNotValidError
from app.db.exceptions import IpAddressNotValidError
from app.db.exceptions import IpError


OP_PATH = "app.db.operations"


class TestOpIp(TestCase):
    """ Unit tests for IpOp class."""

    def test_validate_id_positive(self):
        """ Assumptions:
                - given id is Integer
        """
        positive_id = 1
        try:
            IpOp.validate_id(positive_id)
        except IpError:
            self.fail("Database operations error raised.")

    def test_validate_id_negative(self):
        """ Assumptions:
                - given id is not Integer (String instead)
        """
        negative_id = "1"
        with self.assertRaisesRegex(IpIdNotValidError, "must be Integer"):
            IpOp.validate_id(negative_id)

    def test_validate_address_not_string(self):
        """ Assumptions:
                - given address is not a string
        """
        address = 1111
        with self.assertRaisesRegex(IpAddressNotValidError, "must be String"):
            IpOp.validate_address(address)

    def test_validate_address_regex_not_match(self):
        """ Assumptions:
                - given address does not match respective regex for ip
        """
        wrong_addresses = [
            "0000.0.0.0",
            "0.0000.0.0",
            "0.0.0000.0",
            "0.0.0.0000",
            ".0.0.0",
            "0..0.0",
            "0.0..0",
            "0.0.0..",
        ]
        for wrong_address in wrong_addresses:
            with self.assertRaisesRegex(IpAddressNotValidError, "does not match regex"):
                IpOp.validate_address(wrong_address)

    def test_validate_address_regex_match(self):
        """ Assumptions:
                - given correct IP address match regex.
        """
        good_addresses = ["1.1.1.1", "11.11.11.11", "111.111.111.111"]
        for good_address in good_addresses:
            try:
                IpOp.validate_address(good_address)
            except IpAddressNotValidError:
                self.fail("IpAddressNotValidError raised.")

    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_address")
    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.ip.Ip")
    def test_get_id(self, mock_ip, mock_val_id, mock_val_address):
        """ Assumptions:
                - id argument given
        """
        test_id = 1
        IpOp.get(id=test_id)

        self.assertTrue(mock_val_id.called)
        self.assertFalse(mock_val_address.called)

        self.assertTrue(mock_ip.query.filter_by.called)

        exp_calls = [mock.call(id=test_id), mock.call().all()]
        mock_ip.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_address")
    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.ip.Ip")
    def test_get_address(self, mock_ip, mock_val_id, mock_val_address):
        """ Assumptions:
                - address argument given
        """
        test_address = "test_address"
        IpOp.get(address=test_address)

        self.assertFalse(mock_val_id.called)
        self.assertTrue(mock_val_address.called)

        self.assertTrue(mock_ip.query.filter_by.called)

        exp_calls = [mock.call(address=test_address), mock.call().all()]
        mock_ip.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_address")
    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.ip.Ip")
    def test_get_all_args(self, mock_ip, mock_val_id, mock_val_address):
        """ Assumptions:
                - id argument given
                - address argument given
        """
        test_address = "test_address"
        test_id = 1
        IpOp.get(id=test_id, address=test_address)

        self.assertTrue(mock_val_id.called)
        self.assertTrue(mock_val_address.called)

        self.assertTrue(mock_ip.query.filter_by.called)

        exp_calls = [mock.call(id=test_id, address=test_address), mock.call().all()]
        mock_ip.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.ip.DB")
    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_address")
    @mock.patch(f"{OP_PATH}.basic.ip.Ip")
    def test_add(self, mock_ip, mock_val_address, mock_db):
        """ Assumptions:
                - add method run
        """
        new_name = "Test Name"
        new_ip = IpOp.add(new_name)

        exp_calls = [mock.call(new_name)]
        mock_ip.assert_has_calls(exp_calls)

        self.assertEqual(new_ip, mock_ip())
        self.assertTrue(mock_val_address.called)

        db_exp_calls = [mock.call.session.add(new_ip), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.basic.ip.DB")
    @mock.patch(f"{OP_PATH}.basic.ip.IpOp.validate_address")
    @mock.patch(f"{OP_PATH}.basic.ip.Ip")
    def test_update(self, mock_ip, mock_val_address, mock_db):
        """ Assumptions:
                - update method run
        """
        new_name = "Test Name"
        ip_obj = mock_ip()

        updated_ip = IpOp.update(ip_obj, new_name)

        self.assertTrue(mock_val_address.called)

        db_exp_calls = [mock.call.session.add(updated_ip), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.basic.ip.DB")
    @mock.patch(f"{OP_PATH}.basic.ip.Ip")
    def test_delete(self, mock_ip, mock_db):
        """ Assumptions:
                - delete method run
        """
        ip_obj = mock_ip()

        IpOp.delete(ip_obj)

        db_exp_calls = [mock.call.session.delete(ip_obj), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)
