import re
import string

from unittest import TestCase
from unittest import mock

from app.db.operations.basic.tag import TagOp


OP_PATH = "app.db.operations"


class TestOpTag(TestCase):
    """ Unit tests for TagOp class."""

    def test_validate_id_positive(self):
        """ Assumptions:
                - given id is Integer
        """
        positive_id = 1
        try:
            TagOp.validate_id(positive_id)
        except ValueError:
            self.fail("ValueError raised.")

    def test_validate_id_negative(self):
        """ Assumptions:
                - given id is not Integer (String instead)
        """
        negative_id = "1"
        with self.assertRaisesRegex(ValueError, "must be Integer"):
            TagOp.validate_id(negative_id)

    def test_validate_name_too_short(self):
        """ Assumptions:
                - given name have 0 length
        """
        short_name = ""

        with self.assertRaisesRegex(ValueError, "wrong length"):
            TagOp.validate_name(short_name)

    def test_validate_name_too_long(self):
        """ Assumptions:
                - given name have 16 length
        """
        long_name = "T" * 16

        with self.assertRaisesRegex(ValueError, "wrong length"):
            TagOp.validate_name(long_name)

    def test_validate_name_wrong_type(self):
        """ Assumptions:
                - given name is not String (Integer instead)
        """
        wrong_type_name = 123

        with self.assertRaisesRegex(ValueError, "must be String"):
            TagOp.validate_name(wrong_type_name)

    def test_validate_name_wrong_characters(self):
        """ Assumptions:
                - given name does not match regex [A-Za-z0-9_ ]+
        """
        name_regex = r"[A-Za-z0-9_ ]+"
        wrong_chars = [
            char for char in list(string.printable) if not re.match(name_regex, char)
        ]
        for wrong_char in wrong_chars:
            with self.assertRaisesRegex(ValueError, "does not match regex"):
                TagOp.validate_name(wrong_char)

    def test_validate_name_positive(self):
        """ Assumptions:
                - given name met requirements
        """
        good_name = "Good Name"
        try:
            TagOp.validate_name(good_name)
        except ValueError:
            self.fail("ValueError raised.")

    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.tag.Tag")
    def test_get_id(self, mock_tag, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
        """
        test_id = 1
        TagOp.get(id=test_id)

        self.assertTrue(mock_val_id.called)
        self.assertFalse(mock_val_name.called)

        self.assertTrue(mock_tag.query.filter_by.called)

        exp_calls = [mock.call(id=test_id), mock.call().all()]
        mock_tag.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.tag.Tag")
    def test_get_name(self, mock_tag, mock_val_id, mock_val_name):
        """ Assumptions:
                - name argument given
        """
        test_name = "test_name"
        TagOp.get(name=test_name)

        self.assertFalse(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_tag.query.filter_by.called)

        exp_calls = [mock.call(name=test_name), mock.call().all()]
        mock_tag.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_id")
    @mock.patch(f"{OP_PATH}.basic.tag.Tag")
    def test_get_all_args(self, mock_tag, mock_val_id, mock_val_name):
        """ Assumptions:
                - id argument given
                - name argument given
        """
        test_name = "test_name"
        test_id = 1
        TagOp.get(id=test_id, name=test_name)

        self.assertTrue(mock_val_id.called)
        self.assertTrue(mock_val_name.called)

        self.assertTrue(mock_tag.query.filter_by.called)

        exp_calls = [mock.call(id=test_id, name=test_name), mock.call().all()]
        mock_tag.query.filter_by.assert_has_calls(exp_calls)

    @mock.patch(f"{OP_PATH}.basic.tag.DB")
    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.tag.Tag")
    def test_add(self, mock_tag, mock_val_name, mock_db):
        """ Assumptions:
                - add method run
        """
        new_name = "Test Name"
        new_tag = TagOp.add(new_name)

        exp_calls = [mock.call(new_name)]
        mock_tag.assert_has_calls(exp_calls)

        self.assertEqual(new_tag, mock_tag())

        self.assertTrue(mock_val_name.called)

        db_exp_calls = [mock.call.session.add(new_tag), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.basic.tag.DB")
    @mock.patch(f"{OP_PATH}.basic.tag.TagOp.validate_name")
    @mock.patch(f"{OP_PATH}.basic.tag.Tag")
    def test_update(self, mock_tag, mock_val_name, mock_db):
        """ Assumptions:
                - update method run
        """
        new_name = "Test Name"
        tag_obj = mock_tag()

        updated_admin = TagOp.update(tag_obj, new_name)

        self.assertTrue(mock_val_name.called)

        db_exp_calls = [
            mock.call.session.add(updated_admin),
            mock.call.session.commit(),
        ]

        mock_db.assert_has_calls(db_exp_calls)

    @mock.patch(f"{OP_PATH}.basic.tag.DB")
    @mock.patch(f"{OP_PATH}.basic.tag.Tag")
    def test_delete(self, mock_tag, mock_db):
        """ Assumptions:
                - delete method run
        """
        tag_obj = mock_tag()

        TagOp.delete(tag_obj)

        db_exp_calls = [mock.call.session.delete(tag_obj), mock.call.session.commit()]

        mock_db.assert_has_calls(db_exp_calls)
