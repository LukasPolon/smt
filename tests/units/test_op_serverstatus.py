from unittest import TestCase
from unittest import mock

from app.db.operations.basic.server_status import ServerStatusOp
from app.db.exceptions import ServerStatusIdNotValidError
from app.db.exceptions import ServerStatusNameNotValidError


OP_PATH = "app.db.operations.basic.server_status"


class TestServerStatusOp(TestCase):
    """ Unit tests for ServerStatusOp class."""

    def test_validate_id_positive(self):
        """ Assumptions:
                - given id is Integer
        """
        positive_id = 1
        try:
            ServerStatusOp.validate_id(positive_id)
        except ServerStatusIdNotValidError:
            self.fail("ServerStatusIdNotValidError raised.")

    def test_validate_id_negative(self):
        """ Assumptions:
                - given id is not Integer (String instead)
        """
        negative_id = "1"
        with self.assertRaisesRegex(ServerStatusIdNotValidError, "must be Integer"):
            ServerStatusOp.validate_id(negative_id)

    def test_validate_name_not_string(self):
        """ Assumptions:
                - given name is not a string
        """
        name = 1111
        with self.assertRaisesRegex(ServerStatusNameNotValidError, "must be String"):
            ServerStatusOp.validate_name(name)

    def test_validate_name_too_short(self):
        """ Assumptions:
                - given name have 0 length
        """
        name = ""
        with self.assertRaisesRegex(ServerStatusNameNotValidError, "have wrong length"):
            ServerStatusOp.validate_name(name)

    def test_validate_name_too_long(self):
        """ Assumptions:
                - given name have length == 21
        """
        name = "A" * 21
        with self.assertRaisesRegex(ServerStatusNameNotValidError, "have wrong length"):
            ServerStatusOp.validate_name(name)

    def test_validate_name_good_length(self):
        """ Assumptions:
                - given name have good length (border values)
        """
        names = ["A", "A" * 20]
        for name in names:
            try:
                ServerStatusOp.validate_name(name)
            except ServerStatusNameNotValidError:
                self.fail("ServerStatusNameNotValidError raised.")

    def test_validate_name_incorrect_regex(self):
        """ Assumptions:
                - given name does not match respective regex
        """
        wrong_names = ["A1", "Aa+", "A-", "A!@#$%^&"]
        for wrong_name in wrong_names:
            with self.assertRaisesRegex(
                ServerStatusNameNotValidError, "does not match regex"
            ):
                ServerStatusOp.validate_name(wrong_name)

    def test_validate_name_correct_regex(self):
        """ Assumptions:
                - given correct name match regex.
        """
        good_names = ["Test", "Test_two"]
        for good_name in good_names:
            try:
                ServerStatusOp.validate_name(good_name)
            except ServerStatusNameNotValidError:
                self.fail("ServerStatusNameNotValidError raised.")

    def test_validate_name_not_capital(self):
        """ Assumption:
                - given name have no capital letter at the beginning.
        """
        name = "test"
        with self.assertRaisesRegex(
            ServerStatusNameNotValidError, "must start with capital"
        ):
            ServerStatusOp.validate_name(name)

    def test_validate_name_capital(self):
        """ Assumption:
                - given name have capital letter at the beginning.
        """
        name = "Test"
        try:
            ServerStatusOp.validate_name(name)
        except ServerStatusNameNotValidError:
            self.fail("ServerStatusNameNotValidError raised.")

    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_id")
    @mock.patch(f"{OP_PATH}.ServerStatus")
    def test_get_id(self, mock_servstatus, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
        """
        test_id = 1
        ServerStatusOp.get(id=test_id)

        self.assertTrue(mock_val_id.called)
        self.assertFalse(mock_val_name.called)

        self.assertTrue(mock_servstatus.query.filter_by.called)

        exp_calls = [mock.call(id=test_id), mock.call().all()]
        mock_servstatus.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_id")
    @mock.patch(f"{OP_PATH}.ServerStatus")
    def test_get_name(self, mock_servstatus, mock_val_id, mock_val_name):
        """ Assumptions:
                - name argument given
        """
        test_name = "test_name"
        ServerStatusOp.get(name=test_name)

        self.assertFalse(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_servstatus.query.filter_by.called)

        exp_calls = [mock.call(name=test_name), mock.call().all()]
        mock_servstatus.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_id")
    @mock.patch(f"{OP_PATH}.ServerStatus")
    def test_get_all_args(self, mock_servstatus, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
                - name argument given
        """
        test_name = "test_name"
        test_id = 1
        ServerStatusOp.get(id=test_id, name=test_name)

        self.assertTrue(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_servstatus.query.filter_by.called)

        exp_calls = [mock.call(id=test_id, name=test_name), mock.call().all()]
        mock_servstatus.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerStatus")
    def test_add(self, mock_servstatus, mock_val_name, mock_db):
        """ Assumptions:
                - add method run
        """
        new_name = "TestName"
        new_ip = ServerStatusOp.add(new_name)

        exp_calls = [mock.call(new_name)]
        mock_servstatus.assert_has_calls(exp_calls)

        self.assertEqual(new_ip, mock_servstatus())
        self.assertTrue(mock_val_name.called)

        db_exp_calls = [mock.call.session.add(new_ip), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerStatusOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerStatus")
    def test_update(self, mock_servstatus, mock_val_name, mock_db):
        """ Assumptions:
                - update method run
        """
        new_name = "TestName"
        ip_obj = mock_servstatus()

        updated_ip = ServerStatusOp.update(ip_obj, new_name)

        self.assertTrue(mock_val_name.called)

        db_exp_calls = [mock.call.session.add(updated_ip), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerStatus")
    def test_delete(self, mock_servstatus, mock_db):
        """ Assumptions:
                - delete method run
        """
        ip_obj = mock_servstatus()

        ServerStatusOp.delete(ip_obj)

        db_exp_calls = [mock.call.session.delete(ip_obj), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)
