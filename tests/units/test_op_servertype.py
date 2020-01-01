from unittest import TestCase
from unittest import mock

from app.db.operations.basic.server_type import ServerTypeOp
from app.db.exceptions import ServerTypeIdNotValidError
from app.db.exceptions import ServerTypeNameNotValidError


OP_PATH = "app.db.operations.basic.server_type"


class TestServerTypeOp(TestCase):
    """ Unit tests for ServerTypeOp class."""

    def test_validate_id_positive(self):
        """ Assumptions:
                - given id is Integer
        """
        positive_id = 1
        try:
            ServerTypeOp.validate_id(positive_id)
        except ServerTypeIdNotValidError:
            self.fail("ServerTypeIdNotValidError raised.")

    def test_validate_id_negative(self):
        """ Assumptions:
                - given id is not Integer (String instead)
        """
        negative_id = "1"
        with self.assertRaisesRegex(ServerTypeIdNotValidError, "must be Integer"):
            ServerTypeOp.validate_id(negative_id)

    def test_validate_name_not_string(self):
        """ Assumptions:
                - given name is not a string
        """
        name = 1111
        with self.assertRaisesRegex(ServerTypeNameNotValidError, "must be String"):
            ServerTypeOp.validate_name(name)

    def test_validate_name_too_short(self):
        """ Assumptions:
                - given name have 0 length
        """
        name = ""
        with self.assertRaisesRegex(ServerTypeNameNotValidError, "have wrong length"):
            ServerTypeOp.validate_name(name)

    def test_validate_name_too_long(self):
        """ Assumptions:
                - given name have length == 21
        """
        name = "A" * 21
        with self.assertRaisesRegex(ServerTypeNameNotValidError, "have wrong length"):
            ServerTypeOp.validate_name(name)

    def test_validate_name_good_length(self):
        """ Assumptions:
                - given name have good length (border values)
        """
        names = ["A", "A" * 20]
        for name in names:
            try:
                ServerTypeOp.validate_name(name)
            except ServerTypeNameNotValidError:
                self.fail("ServerTypeNameNotValidError raised.")

    def test_validate_name_incorrect_regex(self):
        """ Assumptions:
                - given name does not match respective regex
        """
        wrong_names = ["A1", "Aa+", "A-", "A!@#$%^&_"]
        for wrong_name in wrong_names:
            with self.assertRaisesRegex(
                ServerTypeNameNotValidError, "does not match regex"
            ):
                ServerTypeOp.validate_name(wrong_name)

    def test_validate_name_correct_regex(self):
        """ Assumptions:
                - given correct name match regex.
        """
        good_names = ["Test", "Test two"]
        for good_name in good_names:
            try:
                ServerTypeOp.validate_name(good_name)
            except ServerTypeNameNotValidError:
                self.fail("ServerTypeNameNotValidError raised.")

    def test_validate_name_not_capital(self):
        """ Assumption:
                - given name have no capital letter at the beginning.
        """
        name = "test"
        with self.assertRaisesRegex(
            ServerTypeNameNotValidError, "must start with capital"
        ):
            ServerTypeOp.validate_name(name)

    def test_validate_name_capital(self):
        """ Assumption:
                - given name have capital letter at the beginning.
        """
        name = "Test"
        try:
            ServerTypeOp.validate_name(name)
        except ServerTypeNameNotValidError:
            self.fail("ServerTypeNameNotValidError raised.")

    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_id")
    @mock.patch(f"{OP_PATH}.ServerType")
    def test_get_id(self, mock_servtype, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
        """
        test_id = 1
        ServerTypeOp.get(id=test_id)

        self.assertTrue(mock_val_id.called)
        self.assertFalse(mock_val_name.called)

        self.assertTrue(mock_servtype.query.filter_by.called)

        exp_calls = [mock.call(id=test_id), mock.call().all()]
        mock_servtype.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_id")
    @mock.patch(f"{OP_PATH}.ServerType")
    def test_get_name(self, mock_servtype, mock_val_id, mock_val_name):
        """ Assumptions:
                - name argument given
        """
        test_name = "test_name"
        ServerTypeOp.get(name=test_name)

        self.assertFalse(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_servtype.query.filter_by.called)

        exp_calls = [mock.call(name=test_name), mock.call().all()]
        mock_servtype.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_id")
    @mock.patch(f"{OP_PATH}.ServerType")
    def test_get_all_args(self, mock_servtype, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
                - name argument given
        """
        test_name = "test_name"
        test_id = 1
        ServerTypeOp.get(id=test_id, name=test_name)

        self.assertTrue(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_servtype.query.filter_by.called)

        exp_calls = [mock.call(id=test_id, name=test_name), mock.call().all()]
        mock_servtype.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerType")
    def test_add(self, mock_servtype, mock_val_name, mock_db):
        """ Assumptions:
                - add method run
        """
        new_name = "TestName"
        new_ip = ServerTypeOp.add(new_name)

        exp_calls = [mock.call(new_name)]
        mock_servtype.assert_has_calls(exp_calls)

        self.assertEqual(new_ip, mock_servtype())
        self.assertTrue(mock_val_name.called)

        db_exp_calls = [mock.call.session.add(new_ip), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerTypeOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerType")
    def test_update(self, mock_servtype, mock_val_name, mock_db):
        """ Assumptions:
                - update method run
        """
        new_name = "TestName"
        ip_obj = mock_servtype()

        updated_ip = ServerTypeOp.update(ip_obj, new_name)

        self.assertTrue(mock_val_name.called)

        db_exp_calls = [mock.call.session.add(updated_ip), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerType")
    def test_delete(self, mock_servtype, mock_db):
        """ Assumptions:
                - delete method run
        """
        ip_obj = mock_servtype()

        ServerTypeOp.delete(ip_obj)

        db_exp_calls = [mock.call.session.delete(ip_obj), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)
