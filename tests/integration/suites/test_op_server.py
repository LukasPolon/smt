from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.server import Server
from app.db.operations.basic.server import ServerOp
from app.db.operations.basic.server_type import ServerTypeOp
from app.db.operations.basic.server_status import ServerStatusOp


@mark.db_operations
@mark.op_server
class TestServerOp(Asserts):
    """ Integration tests for ServerOp class.
        Operations on Server model.
    """

    def case_resolve_status_positive(self, refresh_db_before):
        """ Create ServerStatus rows, then resolve their names into ID."""
        statuses = {"Status_one": 1, "Status_two": 2}
        for status in statuses.keys():
            ServerStatusOp.add(status)

        for status_name, status_key in statuses.items():
            resolved_id = ServerOp.resolve_status(status_name)
            self.assertEqual(status_key, resolved_id)

    def case_resolve_status_not_found(self, refresh_db_before):
        """ Try to resolve ServerStatus row which name does not exist."""
        exception_raised = False
        try:
            ServerOp.resolve_status("Test status")
        except ValueError:
            exception_raised = True

        self.assertTrue(exception_raised)

    def case_resolve_type_positive(self, refresh_db_before):
        """ Create ServerType rows, then resolve their names into ID."""
        types = {"Type one": 1, "Type two": 2}
        for srv_type in types.keys():
            ServerTypeOp.add(srv_type)

        for srv_type_name, srv_type_id in types.items():
            resolved_id = ServerOp.resolve_type(srv_type_name)
            self.assertEqual(srv_type_id, resolved_id)

    def case_resolve_type_not_found(self, refresh_db_before):
        """ Try to resolve ServerType row which name does not exist."""
        exception_raised = False
        try:
            ServerOp.resolve_type("Test type")
        except ValueError:
            exception_raised = True

        self.assertTrue(exception_raised)

    def case_add_with_description(self, refresh_db_before):
        """ Create new Server row with a description field."""
        description = "Some description made. - : *"
        server_name = "TestServer"

        ServerStatusOp.add("TestStatus")
        ServerTypeOp.add("TestType")

        new_server = ServerOp.add(server_name, "TestStatus", "TestType", description)

        get_servers = ServerOp.get()
        self.assertTrue(len(get_servers) is 1)
        self.assertEqual(get_servers[0].description, description)
        self.assertEqual(get_servers[0].id, 1)
        self.assertEqual(get_servers[0].type_id, 1)
        self.assertEqual(get_servers[0].status_id, 1)
        self.assertEqual(get_servers[0].name, server_name)

        self.assertEqual(get_servers[0], new_server)

    def case_add_without_description(self, refresh_db_before):
        """ Create new Server row without description field."""
        server_name = "TestServer"

        ServerStatusOp.add("TestStatus")
        ServerTypeOp.add("TestType")

        new_server = ServerOp.add(server_name, "TestStatus", "TestType")

        get_servers = ServerOp.get()
        self.assertTrue(len(get_servers) is 1)
        self.assertEqual(get_servers[0].description, None)
        self.assertEqual(get_servers[0].id, 1)
        self.assertEqual(get_servers[0].type_id, 1)
        self.assertEqual(get_servers[0].status_id, 1)
        self.assertEqual(get_servers[0].name, server_name)

        self.assertEqual(get_servers[0], new_server)

    def case_get_by_id(self, refresh_db_before):
        """ Get server row with id keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        ServerStatusOp.add("TestStatus")
        ServerTypeOp.add("TestType")

        new_server = ServerOp.add(server_name, "TestStatus", "TestType")

        new_second_server = ServerOp.add(server_second_name, "TestStatus", "TestType")

        get_first_server = ServerOp.get(id=1)

        self.assertTrue(len(get_first_server) is 1)

        self.assertEqual(get_first_server[0], new_server)
        self.assertEqual(get_first_server[0].id, 1)
        self.assertNotEqual(get_first_server[0], new_second_server)

    def case_get_by_name(self, refresh_db_before):
        """ Get server row with name keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        ServerStatusOp.add("TestStatus")
        ServerTypeOp.add("TestType")

        new_server = ServerOp.add(server_name, "TestStatus", "TestType")

        new_second_server = ServerOp.add(server_second_name, "TestStatus", "TestType")

        get_second_server = ServerOp.get(name=server_second_name)

        self.assertTrue(len(get_second_server) is 1)

        self.assertEqual(get_second_server[0], new_second_server)
        self.assertEqual(get_second_server[0].id, 2)
        self.assertNotEqual(get_second_server[0], new_server)

    def case_get_by_srv_status(self, refresh_db_before):
        """ Get server row with srv_status keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        ServerStatusOp.add("StatusOne")
        ServerStatusOp.add("StatusTwo")
        ServerTypeOp.add("TestType")

        srv_one = ServerOp.add(server_name, "StatusOne", "TestType")

        srv_two = ServerOp.add(server_second_name, "StatusTwo", "TestType")

        get_first_status = ServerOp.get(srv_status="StatusOne")
        self.assertTrue(len(get_first_status) is 1)
        self.assertEqual(get_first_status[0].id, 1)
        self.assertEqual(get_first_status[0], srv_one)
        self.assertNotEqual(get_first_status[0], srv_two)

    def case_get_by_srv_type(self, refresh_db_before):
        """ Get server row with srv_type keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("TypeOne")
        ServerTypeOp.add("TypeTwo")

        srv_one = ServerOp.add(server_name, "Status", "TypeOne")

        srv_two = ServerOp.add(server_second_name, "Status", "TypeTwo")

        get_first_type = ServerOp.get(srv_type="TypeOne")
        self.assertTrue(len(get_first_type) is 1)
        self.assertEqual(get_first_type[0].id, 1)
        self.assertEqual(get_first_type[0], srv_one)
        self.assertNotEqual(get_first_type[0], srv_two)

    def case_get_by_all(self, refresh_db_before):
        """ Get server row with both srv_status
            srv_type keywords.
        """
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        server_third_name = "TestServerThree"
        server_fourth_name = "TestServerFour"
        ServerStatusOp.add("StatusOne")
        ServerStatusOp.add("StatusTwo")
        ServerTypeOp.add("TypeOne")
        ServerTypeOp.add("TypeTwo")

        srv_one = ServerOp.add(server_name, "StatusOne", "TypeOne")

        ServerOp.add(server_second_name, "StatusTwo", "TypeTwo")

        ServerOp.add(server_third_name, "StatusOne", "TypeTwo")

        srv_four = ServerOp.add(server_fourth_name, "StatusOne", "TypeOne")

        get_by_all = ServerOp.get(srv_status="StatusOne", srv_type="TypeOne")

        self.assertTrue(len(get_by_all) is 2)
        self.assertEqual(get_by_all[0].id, 1)
        self.assertEqual(get_by_all[1].id, 4)
        self.assertEqual(get_by_all[0], srv_one)
        self.assertEqual(get_by_all[1], srv_four)

    def case_get_without_filters(self, refresh_db_before):
        """ Get server rows without any filters."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("TypeOne")
        ServerTypeOp.add("TypeTwo")

        srv_one = ServerOp.add(server_name, "Status", "TypeOne")

        srv_two = ServerOp.add(server_second_name, "Status", "TypeTwo")

        get_all = ServerOp.get()
        self.assertTrue(len(get_all) is 2)
        self.assertEqual(get_all[0], srv_one)
        self.assertEqual(get_all[1], srv_two)

    def case_update_name(self, refresh_db_before):
        """ Update server name."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("TypeOne")

        srv = ServerOp.add(server_name, "Status", "TypeOne")

        get_before_update = ServerOp.get(name=server_name)
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)

        ServerOp.update(srv, name=server_second_name)

        get_srv = ServerOp.get(name=server_second_name)
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)

    def case_update_srv_status(self, refresh_db_before):
        """ Update server status."""
        server_name = "TestServer"
        ServerStatusOp.add("StatusOne")
        ServerStatusOp.add("StatusTwo")
        ServerTypeOp.add("TypeOne")

        srv = ServerOp.add(server_name, "StatusOne", "TypeOne")

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].status.name, "StatusOne")

        ServerOp.update(srv, srv_status="StatusTwo")

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].status.name, "StatusTwo")

    def case_update_srv_type(self, refresh_db_before):
        """ Update server type."""
        server_name = "TestServer"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("TypeOne")
        ServerTypeOp.add("TypeTwo")

        srv = ServerOp.add(server_name, "Status", "TypeOne")

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].type.name, "TypeOne")

        ServerOp.update(srv, srv_type="TypeTwo")

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].type.name, "TypeTwo")

    def case_update_description(self, refresh_db_before):
        """ Update server description."""
        server_name = "TestServer"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("TypeOne")
        desc_one = "Desc one"
        desc_two = "Desc two"

        srv = ServerOp.add(server_name, "Status", "TypeOne", desc_one)

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].description, desc_one)

        ServerOp.update(srv, description=desc_two)

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].description, desc_two)

    def case_update_all(self, refresh_db_before):
        """ Update all fields."""
        server_name = "TestServer"
        server_name_two = "TestServerTwo"
        ServerStatusOp.add("Status")
        ServerStatusOp.add("StatusTwo")
        ServerTypeOp.add("TypeOne")
        ServerTypeOp.add("TypeTwo")
        desc_one = "Desc one"
        desc_two = "Desc two"

        srv = ServerOp.add(server_name, "Status", "TypeOne", desc_one)

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].name, server_name)
        self.assertEqual(get_before_update[0].description, desc_one)
        self.assertEqual(get_before_update[0].status.name, "Status")
        self.assertEqual(get_before_update[0].type.name, "TypeOne")

        ServerOp.update(
            srv,
            name=server_name_two,
            description=desc_two,
            srv_status="StatusTwo",
            srv_type="TypeTwo",
        )

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].name, server_name_two)
        self.assertEqual(get_srv[0].description, desc_two)
        self.assertEqual(get_srv[0].status.name, "StatusTwo")
        self.assertEqual(get_srv[0].type.name, "TypeTwo")

    def case_delete(self, refresh_db_before):
        """ Delete record."""
        server_name = "TestServer"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("TypeOne")

        ServerOp.add(server_name, "Status", "TypeOne")

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].name, server_name)

        ServerOp.delete(get_srv[0])
        get_empty = ServerOp.get()
        self.assertFalse(get_empty)
