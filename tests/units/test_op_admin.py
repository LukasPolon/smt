from unittest import TestCase
from unittest import mock

from app.db.operations.basic.admin import AdminOp
from app.db.exceptions import AdminIdNotValidError
from app.db.exceptions import AdminNameNotValidError
from app.db.exceptions import DbError


OP_PATH = "app.db.operations"


class TestOpAdmin(TestCase):
    """ Unit tests for AdminOp class."""

    def test_validate_id_positive(self):
        """ Assumptions:
                - given id is Integer
        """
        positive_id = 1
        try:
            AdminOp.validate_id(positive_id)
        except DbError:
            self.fail("Database error raised.")

    def test_validate_id_negative(self):
        """ Assumptions:
                - given id is not Integer (String instead)
        """
        negative_id = "1"
        with self.assertRaisesRegex(AdminIdNotValidError, "must be Integer"):
            AdminOp.validate_id(negative_id)

    def test_validate_name_too_short(self):
        """ Assumptions:
                - given name have 0 length
        """
        short_name = ""

        with self.assertRaisesRegex(AdminNameNotValidError, "wrong length"):
            AdminOp.validate_name(short_name)

    def test_validate_name_too_long(self):
        """ Assumptions:
                - given name have 21 length
        """
        long_name = "T" * 21

        with self.assertRaisesRegex(AdminNameNotValidError, "wrong length"):
            AdminOp.validate_name(long_name)

    def test_validate_name_wrong_type(self):
        """ Assumptions:
                - given name is not String (Integer instead)
        """
        wrong_type_name = 123

        with self.assertRaisesRegex(AdminNameNotValidError, "must be String"):
            AdminOp.validate_name(wrong_type_name)

    def test_validate_name_wrong_characters(self):
        """ Assumptions:
                - given name contains incorrect characters
        """
        wrong_chars_names = ["(", ")", "_", "-", "*", "$"]

        for char in wrong_chars_names:
            with self.assertRaisesRegex(AdminNameNotValidError, "does not match regex"):
                AdminOp.validate_name(char)

    def test_validate_name_positive(self):
        """ Assumptions:
                - given name met requirements
        """
        good_name = "Good Name"
        try:
            AdminOp.validate_name(good_name)
        except DbError:
            self.fail("Database error raised.")

    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.admin.Admin")
    def test_get_id(self, mock_admin, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
        """
        test_id = 1
        AdminOp.get(id=test_id)

        self.assertTrue(mock_val_id.called)
        self.assertFalse(mock_val_name.called)

        self.assertTrue(mock_admin.query.filter_by.called)

        exp_calls = [mock.call(id=test_id), mock.call().all()]
        mock_admin.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.admin.Admin")
    def test_get_name(self, mock_admin, mock_val_id, mock_val_name):
        """ Assumptions:
                - name argument given
        """
        test_name = "test_name"
        AdminOp.get(name=test_name)

        self.assertFalse(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_admin.query.filter_by.called)

        exp_calls = [mock.call(name=test_name), mock.call().all()]
        mock_admin.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.admin.Admin")
    def test_get_all_args(self, mock_admin, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
                - name argument given
        """
        test_name = "test_name"
        test_id = 1
        AdminOp.get(id=test_id, name=test_name)

        self.assertTrue(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_admin.query.filter_by.called)

        exp_calls = [mock.call(id=test_id, name=test_name), mock.call().all()]
        mock_admin.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.admin.DB")
    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.admin.Admin")
    def test_add(self, mock_admin, mock_val_name, mock_db):
        """ Assumptions:
                - add method run
        """
        new_name = "Test Name"
        new_admin = AdminOp.add(new_name)

        exp_calls = [mock.call(new_name)]
        mock_admin.assert_has_calls(exp_calls)

        self.assertEqual(new_admin, mock_admin())

        self.assertTrue(mock_val_name.called)

        db_exp_calls = [mock.call.session.add(new_admin), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.basic.admin.DB")
    @mock.patch(f"{OP_PATH}.basic.admin.AdminOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.admin.Admin")
    def test_update(self, mock_admin, mock_val_name, mock_db):
        """ Assumptions:
                - update method run
        """
        new_name = "Test Name"
        admin_obj = mock_admin()

        updated_admin = AdminOp.update(admin_obj, new_name)

        self.assertTrue(mock_val_name.called)

        db_exp_calls = [
            mock.call.session.add(updated_admin),
            mock.call.session.commit(),
        ]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.basic.admin.DB")
    @mock.patch(f"{OP_PATH}.basic.admin.Admin")
    def test_delete(self, mock_admin, mock_db):
        """ Assumptions:
                - delete method run
        """
        admin_obj = mock_admin()

        AdminOp.delete(admin_obj)

        db_exp_calls = [mock.call.session.delete(admin_obj), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)
