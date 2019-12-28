import re
import string

from unittest import TestCase
from unittest import mock

from app.db.operations.basic.server import ServerOp


OP_PATH = "app.db.operations.basic.server"


class TestServerOp(TestCase):
    """ Unit tests for ServerOp class."""

    def test_validate_id_positive(self):
        """ Assumptions:
                - given id is Integer
        """
        positive_id = 1
        try:
            ServerOp.validate_id(positive_id)
        except ValueError:
            self.fail("ValueError raised.")

    def test_validate_id_negative(self):
        """ Assumptions:
                - given id is not Integer (String instead)
        """
        negative_id = "1"
        with self.assertRaisesRegex(ValueError, "must be Integer"):
            ServerOp.validate_id(negative_id)

    def test_validate_name_positive(self):
        """ Assumptions:
                - given name is string with length >= 1 and <= 30
                  and matched regex [A-Za-z0-9_]+
        """
        name = "aA09_"
        try:
            ServerOp.validate_name(name)
        except ValueError:
            self.fail("ValueError raised.")

    def test_validate_name_not_string(self):
        """ Assumptions:
                - given name is not string (int instead)
        """
        name = 111
        with self.assertRaisesRegex(ValueError, "must be String"):
            ServerOp.validate_name(name)

    def test_validate_name_too_short(self):
        """ Assumptions:
                - given name have 0 length
        """
        name = ""
        with self.assertRaisesRegex(ValueError, "wrong length"):
            ServerOp.validate_name(name)

    def test_validate_name_too_long(self):
        """ Assumptions:
                - given name have 31 length
        """
        name = "a" * 31
        with self.assertRaisesRegex(ValueError, "wrong length"):
            ServerOp.validate_name(name)

    def test_validate_name_wrong_characters(self):
        """ Assumptions:
                - given name does not match regex [A-Za-z0-9_]+
        """
        name_regex = r"[A-Za-z0-9_]+"
        wrong_chars = [
            char for char in list(string.printable) if not re.match(name_regex, char)
        ]
        for wrong_char in wrong_chars:
            with self.assertRaisesRegex(ValueError, "does not match regex"):
                ServerOp.validate_name(wrong_char)

    def test_validate_description_positive(self):
        """ Assumptions:
                - given description is string with length >= 1 and <= 60
                  and matched regex [A-Za-z0-9_]+
        """
        desc = "aA09_"
        try:
            ServerOp.validate_description(desc)
        except ValueError:
            self.fail("ValueError raised.")

    def test_validate_description_not_string(self):
        """ Assumptions:
                - given description is not string (int instead)
        """
        desc = 111
        with self.assertRaisesRegex(ValueError, "must be String"):
            ServerOp.validate_description(desc)

    def test_validate_description_too_short(self):
        """ Assumptions:
                - given description have 0 length
        """
        desc = ""
        with self.assertRaisesRegex(ValueError, "wrong length"):
            ServerOp.validate_description(desc)

    def test_validate_description_too_long(self):
        """ Assumptions:
                - given description have 61 length
        """
        desc = "a" * 61
        with self.assertRaisesRegex(ValueError, "wrong length"):
            ServerOp.validate_description(desc)

    def test_validate_description_wrong_characters(self):
        """ Assumptions:
                - given description does not match regex [A-Za-z0-9_ ]+
        """
        name_regex = r"[A-Za-z0-9_ ]+"
        wrong_chars = [
            char for char in list(string.printable) if not re.match(name_regex, char)
        ]
        for wrong_char in wrong_chars:
            with self.assertRaisesRegex(ValueError, "does not match regex"):
                ServerOp.validate_description(wrong_char)

    @mock.patch(f"{OP_PATH}.ServerStatusOp")
    def test_resolve_status_positive(self, mock_status_op):
        """ Assumptions:
                - ServerStatusOp.get() returns one record
        """
        mock_status = mock.MagicMock()
        mock_status.id = 1
        mock_status_op.get.return_value = [mock_status]

        status_id = ServerOp.resolve_status("status_name")

        self.assertEqual(mock_status.id, status_id)
        mock_status_get_calls = [mock.call(name="status_name")]

        mock_status_op.get.assert_has_calls(mock_status_get_calls)

    @mock.patch(f"{OP_PATH}.ServerStatusOp")
    def test_resolve_status_not_found(self, mock_status_op):
        """ Assumptions:
                - ServerStatusOp.get() returns no records
        """
        mock_status_op.get.return_value = list()

        with self.assertRaisesRegex(ValueError, "Not found"):
            ServerOp.resolve_status("status_name")

        mock_status_get_calls = [mock.call(name="status_name")]
        mock_status_op.get.assert_has_calls(mock_status_get_calls)

    @mock.patch(f"{OP_PATH}.ServerTypeOp")
    def test_resolve_type_positive(self, mock_type_op):
        """ Assumptions:
                ServerTypeOp.get() returns one record
        """
        mock_type = mock.MagicMock()
        mock_type.id = 1
        mock_type_op.get.return_value = [mock_type]

        status_id = ServerOp.resolve_type("TypeName")

        self.assertEqual(mock_type.id, status_id)
        mock_status_get_calls = [mock.call(name="TypeName")]

        mock_type_op.get.assert_has_calls(mock_status_get_calls)

    @mock.patch(f"{OP_PATH}.ServerTypeOp")
    def test_resolve_type_not_found(self, mock_type_op):
        """ Assumptions:
                - ServerTypeOp.get() returns no records
        """
        mock_type_op.get.return_value = list()

        with self.assertRaisesRegex(ValueError, "Not found"):
            ServerOp.resolve_type("TypeName")

        mock_status_get_calls = [mock.call(name="TypeName")]
        mock_type_op.get.assert_has_calls(mock_status_get_calls)

    @mock.patch(f"{OP_PATH}.IpOp")
    def test_resolve_ip_positive(self, mock_ip_op):
        """ Assumptions:
                - IpOp.get() returns one record
        """
        mock_ip = mock.MagicMock()
        mock_ip_op.get.return_value = [mock_ip]

        resolved_ip_obj = ServerOp.resolve_ip("11.11.11.11")
        self.assertEqual(resolved_ip_obj, mock_ip)

        mock_ip_get_calls = [mock.call(address="11.11.11.11")]
        mock_ip_op.get.assert_has_calls(mock_ip_get_calls)

    @mock.patch(f"{OP_PATH}.IpOp")
    def test_resolve_ip_not_found(self, mock_ip_op):
        """ Assumptions:
                - IpOp.get() returns no records
        """
        mock_ip_op.get.return_value = list()

        with self.assertRaisesRegex(ValueError, "Not found"):
            ServerOp.resolve_ip("11.11.11.11")

        mock_ip_get_calls = [mock.call(address="11.11.11.11")]
        mock_ip_op.get.assert_has_calls(mock_ip_get_calls)

    @mock.patch(f"{OP_PATH}.TagOp")
    def test_resolve_tag_positive(self, mock_tag_op):
        """ Assumptions:
                - TagOp.get() returns one record
        """
        mock_tag = mock.MagicMock()
        mock_tag_op.get.return_value = [mock_tag]

        resolved_tag_obj = ServerOp.resolve_tag("tag")
        self.assertEqual(resolved_tag_obj, mock_tag)

        mock_tag_get_calls = [mock.call(name="tag")]
        mock_tag_op.get.assert_has_calls(mock_tag_get_calls)

    @mock.patch(f"{OP_PATH}.TagOp")
    def test_resolve_tag_not_found(self, mock_tag_op):
        """ Assumptions:
                - TagOp.get() returns no records
        """
        mock_tag_op.get.return_value = list()

        with self.assertRaisesRegex(ValueError, "Not found"):
            ServerOp.resolve_tag("tag")

        mock_tag_get_calls = [mock.call(name="tag")]
        mock_tag_op.get.assert_has_calls(mock_tag_get_calls)

    @mock.patch(f"{OP_PATH}.AdminOp")
    def test_resolve_admin_positive(self, mock_admin_op):
        """ Assumptions:
                - AdminOp.get() returns one record
        """
        mock_admin = mock.MagicMock()
        mock_admin_op.get.return_value = [mock_admin]

        resolved_adm_obj = ServerOp.resolve_admin("admin")
        self.assertEqual(resolved_adm_obj, mock_admin)

        mock_adm_get_calls = [mock.call(name="admin")]
        mock_admin_op.get.assert_has_calls(mock_adm_get_calls)

    @mock.patch(f"{OP_PATH}.AdminOp")
    def test_resolve_admin_not_found(self, mock_admin_op):
        """ Assumptions:
                - AdminOp.get() returns no records
        """
        mock_admin_op.get.return_value = list()

        with self.assertRaisesRegex(ValueError, "Not found"):
            ServerOp.resolve_admin("admin")

        mock_adm_get_calls = [mock.call(name="admin")]
        mock_admin_op.get.assert_has_calls(mock_adm_get_calls)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_id(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: id
        """
        exp_mock = mock_server.query.filter_by().all()
        result = ServerOp.get(id=1)
        self.assertEqual(exp_mock, result)

        self.assertTrue(mock_val_id.called)
        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_name(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: name
        """
        exp_mock = mock_server.query.filter_by().all()
        result = ServerOp.get(name="Name")
        self.assertEqual(exp_mock, result)

        self.assertFalse(mock_val_id.called)
        self.assertTrue(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_srv_status(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: srv_status
        """
        exp_mock = mock_server.query.filter_by().all()
        result = ServerOp.get(srv_status="Status")
        self.assertEqual(exp_mock, result)

        self.assertFalse(mock_val_id.called)
        self.assertFalse(mock_val_name.called)
        self.assertTrue(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_srv_type(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: srv_type
        """
        exp_mock = mock_server.query.filter_by().all()
        result = ServerOp.get(srv_type="Type")
        self.assertEqual(exp_mock, result)

        self.assertFalse(mock_val_id.called)
        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertTrue(mock_res_type.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_ip(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: ip
        """
        mock_ip_obj = mock.MagicMock(name="MockIpObj")
        mock_res_ip.return_value = mock_ip_obj

        mock_srv = mock.MagicMock(name="MockSrv")
        mock_srv.ips = [mock_ip_obj]

        mock_server.query.filter_by().all.return_value = [mock_srv]

        result = ServerOp.get(ip="11.11.11.11")
        self.assertEqual([mock_srv], result)

        self.assertFalse(mock_val_id.called)
        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertTrue(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_tags(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: tags
        """
        mock_tag_obj = mock.MagicMock(name="MockTagObj")
        mock_res_tag.return_value = mock_tag_obj

        mock_srv = mock.MagicMock(name="MockSrv")
        mock_srv.tags = [mock_tag_obj]

        mock_server.query.filter_by().all.return_value = [mock_srv]

        result = ServerOp.get(tags=["tag"])
        self.assertEqual([mock_srv], result)

        self.assertFalse(mock_val_id.called)
        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_res_ip.called)
        self.assertTrue(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def test_get_by_admins(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used filter: admins
        """
        mock_adm_obj = mock.MagicMock(name="MockAdmObj")
        mock_res_adm.return_value = mock_adm_obj

        mock_srv = mock.MagicMock(name="MockSrv")
        mock_srv.admins = [mock_adm_obj]

        mock_server.query.filter_by().all.return_value = [mock_srv]

        result = ServerOp.get(admins=["admin"])
        self.assertEqual([mock_srv], result)

        self.assertFalse(mock_val_id.called)
        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertTrue(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_id")
    def get_by_all(
        self,
        mock_val_id,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
    ):
        """ Assumptions:
                - used all filters
        """
        exp_mock = mock_server.query.filter_by().all()
        result = ServerOp.get(
            id=1,
            name="Name",
            srv_status="Status",
            srv_type="Type",
            ip="11.11.11.11",
            tags=["tag"],
            admins=["admin"],
        )
        self.assertEqual(exp_mock, result)

        self.assertTrue(mock_val_id.called)
        self.assertTrue(mock_val_name.called)
        self.assertTrue(mock_res_status.called)
        self.assertTrue(mock_res_type.called)
        self.assertTrue(mock_res_ip.called)
        self.assertTrue(mock_res_tag.called)
        self.assertTrue(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_add_basic(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
        mock_db,
    ):
        """ Add new Server record without ip and tags."""
        result = ServerOp.add("Name", "SrvStatus", "SrvType")
        self.assertEqual(result, mock_server())

        self.assertTrue(mock_val_name.called)
        self.assertTrue(mock_res_type.called)
        self.assertTrue(mock_res_status.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)
        self.assertFalse(mock_res_adm.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_add_with_ips(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
        mock_db,
    ):
        """ Add new Server record with ip."""
        result = ServerOp.add("Name", "SrvStatus", "SrvType", ips=["11.11.11.11"])
        self.assertEqual(result, mock_server())

        self.assertTrue(mock_val_name.called)
        self.assertTrue(mock_res_type.called)
        self.assertTrue(mock_res_status.called)

        self.assertTrue(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_add_with_tags(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
        mock_db,
    ):
        """ Add new Server record with tags."""
        result = ServerOp.add("Name", "SrvStatus", "SrvType", tags=["tags"])
        self.assertEqual(result, mock_server())

        self.assertTrue(mock_val_name.called)
        self.assertTrue(mock_res_type.called)
        self.assertTrue(mock_res_status.called)

        self.assertFalse(mock_res_ip.called)
        self.assertTrue(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.Server")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_add_with_admins(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_server,
        mock_db,
    ):
        """ Add new Server record with admins."""
        result = ServerOp.add("Name", "SrvStatus", "SrvType", admins=["admin"])
        self.assertEqual(result, mock_server())

        self.assertTrue(mock_val_name.called)
        self.assertTrue(mock_res_type.called)
        self.assertTrue(mock_res_status.called)

        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertTrue(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_name(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update name in the existing record."""
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.name = "TestNameOne"

        mock_updated = ServerOp.update(mock_srv_obj, name="TestNameTwo")

        self.assertEqual(mock_updated.name, "TestNameTwo")

        self.assertTrue(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_val_desc.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_srv_status(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update srv_status in the existing record."""
        mock_res_status.return_value = 222
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.status_id = 111

        mock_updated = ServerOp.update(mock_srv_obj, srv_status="SrvStat")

        self.assertEqual(mock_updated.status_id, 222)

        self.assertFalse(mock_val_name.called)
        self.assertTrue(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_val_desc.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_srv_type(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update srv_type in the existing record."""
        mock_res_type.return_value = 222
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.type_id = 111

        mock_updated = ServerOp.update(mock_srv_obj, srv_type="SrvType")

        self.assertEqual(mock_updated.type_id, 222)

        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertTrue(mock_res_type.called)
        self.assertFalse(mock_val_desc.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_description(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update description in the existing record."""
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.description = "DescOne"

        mock_updated = ServerOp.update(mock_srv_obj, description="DescTwo")

        self.assertEqual(mock_updated.description, "DescTwo")

        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertTrue(mock_val_desc.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_ips(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update ip addresses in the existing record."""
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.ips = ["11.11.11.11"]

        mock_updated = ServerOp.update(mock_srv_obj, ips=["22.22.22.22"])

        self.assertEqual(mock_updated.ips, [mock_res_ip()])

        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_val_desc.called)
        self.assertTrue(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_tags(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update tags in the existing record."""
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.tags = ["tag"]

        mock_updated = ServerOp.update(mock_srv_obj, tags=["tag"])

        self.assertEqual(mock_updated.tags, [mock_res_tag()])

        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_val_desc.called)
        self.assertFalse(mock_res_ip.called)
        self.assertTrue(mock_res_tag.called)
        self.assertFalse(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_admin")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_tag")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_ip")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_description")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_type")
    @mock.patch(f"{OP_PATH}.ServerOp.resolve_status")
    @mock.patch(f"{OP_PATH}.ServerOp.validate_name")
    def test_update_admins(
        self,
        mock_val_name,
        mock_res_status,
        mock_res_type,
        mock_val_desc,
        mock_res_ip,
        mock_res_tag,
        mock_res_adm,
        mock_db,
    ):
        """ Update admins in the existing record."""
        mock_srv_obj = mock.MagicMock()
        mock_srv_obj.admins = ["adm"]

        mock_updated = ServerOp.update(mock_srv_obj, admins=["adm"])

        self.assertEqual(mock_updated.admins, [mock_res_adm()])

        self.assertFalse(mock_val_name.called)
        self.assertFalse(mock_res_status.called)
        self.assertFalse(mock_res_type.called)
        self.assertFalse(mock_val_desc.called)
        self.assertFalse(mock_res_ip.called)
        self.assertFalse(mock_res_tag.called)
        self.assertTrue(mock_res_adm.called)

        self.assertTrue(mock_db.session.add.called)
        self.assertTrue(mock_db.session.commit.called)

    @mock.patch(f"{OP_PATH}.DB")
    def test_detele(self, mock_db):
        """ Delete record."""
        mock_srv_obj = mock.MagicMock()

        ServerOp.delete(mock_srv_obj)

        self.assertTrue(mock_db.session.delete.called)
        self.assertTrue(mock_db.session.commit.called)
