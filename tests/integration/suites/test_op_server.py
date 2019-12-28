from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.server import Server
from app.db.models.ip import Ip
from app.db.operations.basic.ip import IpOp
from app.db.operations.basic.tag import TagOp
from app.db.operations.basic.admin import AdminOp
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

    def case_resolve_ip_positive(self, refresh_db_before):
        """ Try to resolve Ip row."""
        ips = ["11.11.11.11", "22.22.22.22", "33.33.33.33"]
        for ip in ips:
            IpOp.add(address=ip)

        for id, ip in enumerate(ips):
            ip_obj = ServerOp.resolve_ip(ip)
            self.assertEqual(ip_obj.id, id + 1)
            self.assertEqual(ip_obj.address, ip)
            self.assertTrue(isinstance(ip_obj, Ip))

    def case_resolve_ip_not_found(self, refresh_db_before):
        """ Try to resolve Ip row which does not exists."""
        exception_raised = False
        try:
            ServerOp.resolve_ip("11.11.11.11")
        except ValueError:
            exception_raised = True

        self.assertTrue(exception_raised)

    def case_resolve_tag_positive(self, refresh_db_before):
        """ Try to resolve existing Tag name."""
        tag_name = "new tag"
        tag_obj = TagOp.add(tag_name)

        tag_res_obj = ServerOp.resolve_tag(tag_name)
        self.assertEqual(tag_obj, tag_res_obj)
        self.assertEqual(tag_res_obj.name, tag_name)

    def case_resolve_tag_not_found(self, refresh_db_before):
        """ Try to resolve non-existing tag name."""
        exception_raised = False
        try:
            ServerOp.resolve_tag("not-existing tag")
        except ValueError:
            exception_raised = True

        self.assertTrue(exception_raised)

    def case_resolve_admin_positive(self, refresh_db_before):
        """ Try to resolve existing Admin name."""
        adm_name = "New Admin"
        adm_obj = AdminOp.add(adm_name)

        adm_res_obj = ServerOp.resolve_admin(adm_name)
        self.assertEqual(adm_obj, adm_res_obj)
        self.assertEqual(adm_res_obj.name, adm_name)

    def case_resolve_admin_not_found(self, refresh_db_before):
        """ Try to resolve non-existing admin name."""
        exception_raised = False
        try:
            ServerOp.resolve_admin("Adm")
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

    def case_add_with_ips(self, refresh_db_before):
        """ Create new Server row with ips many-to-many relation."""
        server_name = "TestServer"
        server_status = "TestStatus"
        server_type = "TestType"
        ips = ["11.11.11.11", "22.22.22.22", "33.33.33.33"]

        ServerStatusOp.add(server_status)
        ServerTypeOp.add(server_type)
        for ip in ips:
            IpOp.add(ip)

        new_server = ServerOp.add(server_name, server_status, server_type, ips=ips)

        get_servers = ServerOp.get()
        self.assertTrue(len(get_servers) is 1)
        self.assertEqual(get_servers[0].description, None)
        self.assertEqual(get_servers[0].id, 1)
        self.assertEqual(get_servers[0].name, server_name)
        self.assertEqual(get_servers[0], new_server)

        for srv_ip, exp_ip in zip(get_servers[0].ips, ips):
            self.assertEqual(srv_ip.address, exp_ip)

    def case_add_with_tags(self, refresh_db_before):
        """ Create new Server row with tags many-to-many relation."""
        server_name = "TestServer"
        server_status = "TestStatus"
        server_type = "TestType"
        tags = ["tag one", "tag two", "tag three"]

        ServerStatusOp.add(server_status)
        ServerTypeOp.add(server_type)
        for tag in tags:
            TagOp.add(tag)

        new_server = ServerOp.add(server_name, server_status, server_type, tags=tags)

        get_servers = ServerOp.get()
        self.assertTrue(len(get_servers) is 1)
        self.assertEqual(get_servers[0].description, None)
        self.assertEqual(get_servers[0].id, 1)
        self.assertEqual(get_servers[0].name, server_name)
        self.assertEqual(get_servers[0], new_server)

        for tag, exp_name in zip(get_servers[0].tags, tags):
            self.assertEqual(tag.name, exp_name)

    def case_add_with_admins(self, refresh_db_before):
        """ Create new Server row with admins many-to-many relation."""
        server_name = "TestServer"
        server_status = "TestStatus"
        server_type = "TestType"
        admins = ["Admin One", "Admin Two"]

        ServerStatusOp.add(server_status)
        ServerTypeOp.add(server_type)
        for admin in admins:
            AdminOp.add(admin)

        new_server = ServerOp.add(
            server_name, server_status, server_type, admins=admins
        )

        get_servers = ServerOp.get()
        self.assertTrue(len(get_servers) is 1)
        self.assertEqual(get_servers[0].description, None)
        self.assertEqual(get_servers[0].id, 1)
        self.assertEqual(get_servers[0].name, server_name)
        self.assertEqual(get_servers[0], new_server)

        for admin, exp_name in zip(get_servers[0].admins, admins):
            self.assertEqual(admin.name, exp_name)

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

    def case_get_by_ip(self, refresh_db_before):
        """ Get server row with ip keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        server_status = "TestStatus"
        server_type = "TestType"
        ServerStatusOp.add(server_status)
        ServerTypeOp.add(server_type)

        ips = ["11.11.11.11", "22.22.22.22"]
        for ip in ips:
            IpOp.add(ip)

        srv_one = ServerOp.add(server_name, server_status, server_type, ips=[ips[0]])
        srv_two = ServerOp.add(
            server_second_name, server_status, server_type, ips=[ips[1]]
        )

        get_first_ip = ServerOp.get(ip=ips[0])
        self.assertTrue(len(get_first_ip) is 1)
        self.assertEqual(get_first_ip[0], srv_one)
        self.assertNotEqual(get_first_ip[0], srv_two)
        self.assertTrue(len(get_first_ip[0].ips) is 1)
        self.assertEqual(get_first_ip[0].ips[0].address, ips[0])

    def case_get_by_tags(self, refresh_db_before):
        """ Get server row with tags keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        server_status = "TestStatus"
        server_type = "TestType"
        ServerStatusOp.add(server_status)
        ServerTypeOp.add(server_type)

        tags = ["tag one", "tag two", "tag three"]
        for tag in tags:
            TagOp.add(tag)

        srv_one = ServerOp.add(
            server_name, server_status, server_type, tags=[tags[0], tags[1]]
        )
        srv_two = ServerOp.add(
            server_second_name, server_status, server_type, tags=tags
        )

        get_lonely = ServerOp.get(tags=[tags[2]])
        self.assertTrue(len(get_lonely) is 1)
        self.assertEqual(get_lonely[0], srv_two)
        self.assertEqual(len(get_lonely[0].tags), len(tags))

        get_all = ServerOp.get(tags=[tags[0]])
        self.assertTrue(len(get_all) is 2)

    def case_get_by_admins(self, refresh_db_before):
        """ Get server row with admins keyword."""
        server_name = "TestServer"
        server_second_name = "TestServerTwo"
        server_status = "TestStatus"
        server_type = "TestType"
        ServerStatusOp.add(server_status)
        ServerTypeOp.add(server_type)

        admins = ["Admin One", "Admin Two", "Admin Three"]
        for admin in admins:
            AdminOp.add(admin)

        srv_one = ServerOp.add(
            server_name, server_status, server_type, admins=[admins[0], admins[1]]
        )
        srv_two = ServerOp.add(
            server_second_name, server_status, server_type, admins=admins
        )

        get_lonely = ServerOp.get(admins=[admins[2]])
        self.assertTrue(len(get_lonely) is 1)
        self.assertEqual(get_lonely[0], srv_two)
        self.assertEqual(len(get_lonely[0].admins), len(admins))

        get_all = ServerOp.get(admins=[admins[0]])
        self.assertTrue(len(get_all) is 2)

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

        IpOp.add("11.11.11.11")
        IpOp.add("22.22.22.22")

        TagOp.add("Tag one")
        TagOp.add("Tag two")

        AdminOp.add("Admin One")
        AdminOp.add("Admin Two")

        srv_one = ServerOp.add(
            server_name,
            "StatusOne",
            "TypeOne",
            ips=["11.11.11.11"],
            tags=["Tag one"],
            admins=["Admin One"],
        )

        ServerOp.add(
            server_second_name,
            "StatusTwo",
            "TypeTwo",
            ips=["22.22.22.22"],
            tags=["Tag two"],
            admins=["Admin Two"],
        )

        ServerOp.add(
            server_third_name,
            "StatusOne",
            "TypeTwo",
            ips=["22.22.22.22"],
            tags=["Tag two"],
            admins=["Admin Two"],
        )

        srv_four = ServerOp.add(
            server_fourth_name,
            "StatusOne",
            "TypeOne",
            ips=["11.11.11.11"],
            tags=["Tag one"],
            admins=["Admin One"],
        )

        get_by_all = ServerOp.get(
            srv_status="StatusOne",
            srv_type="TypeOne",
            ip="11.11.11.11",
            tags=["Tag one"],
            admins=["Admin One"],
        )

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

    def case_update_ips(self, refresh_db_before):
        """ Update ip addresses. """
        server_name = "TestServer"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("Type")
        ips_one = IpOp.add("11.11.11.11")
        ips_two = IpOp.add("22.22.22.22")

        srv = ServerOp.add(server_name, "Status", "Type", ips=["11.11.11.11"])

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].ips, [ips_one])

        ServerOp.update(srv, ips=["22.22.22.22"])

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].ips, [ips_two])

    def case_update_tags(self, refresh_db_before):
        """ Update tags."""
        server_name = "TestServer"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("Type")

        tag_one = TagOp.add("tag one")
        tag_two = TagOp.add("tag two")

        srv = ServerOp.add(server_name, "Status", "Type", tags=["tag one"])

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].tags, [tag_one])

        ServerOp.update(srv, tags=["tag two"])

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].tags, [tag_two])

    def case_update_admins(self, refresh_db_before):
        """ Update admins."""
        server_name = "TestServer"
        ServerStatusOp.add("Status")
        ServerTypeOp.add("Type")

        admin_one = AdminOp.add("Admin One")
        admin_two = AdminOp.add("Admin Two")

        srv = ServerOp.add(server_name, "Status", "Type", admins=["Admin One"])

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].admins, [admin_one])

        ServerOp.update(srv, admins=["Admin Two"])

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].admins, [admin_two])

    @mark.one
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
        ips_one = IpOp.add("11.11.11.11")
        ips_two = IpOp.add("22.22.22.22")
        tag_one = TagOp.add("tag one")
        tag_two = TagOp.add("tag two")
        admin_one = AdminOp.add("Admin One")
        admin_two = AdminOp.add("Admin Two")

        srv = ServerOp.add(
            server_name,
            "Status",
            "TypeOne",
            description=desc_one,
            ips=["11.11.11.11"],
            tags=["tag one"],
            admins=["Admin One"],
        )

        get_before_update = ServerOp.get()
        self.assertTrue(len(get_before_update) is 1)
        self.assertEqual(get_before_update[0].id, 1)
        self.assertEqual(get_before_update[0].name, server_name)
        self.assertEqual(get_before_update[0].description, desc_one)
        self.assertEqual(get_before_update[0].status.name, "Status")
        self.assertEqual(get_before_update[0].type.name, "TypeOne")
        self.assertEqual(get_before_update[0].ips, [ips_one])
        self.assertEqual(get_before_update[0].tags, [tag_one])
        self.assertEqual(get_before_update[0].admins, [admin_one])

        ServerOp.update(
            srv,
            name=server_name_two,
            description=desc_two,
            srv_status="StatusTwo",
            srv_type="TypeTwo",
            ips=["22.22.22.22"],
            tags=["tag two"],
            admins=["Admin Two"],
        )

        get_srv = ServerOp.get()
        self.assertTrue(len(get_srv) is 1)
        self.assertEqual(get_srv[0].id, 1)
        self.assertEqual(get_srv[0].name, server_name_two)
        self.assertEqual(get_srv[0].description, desc_two)
        self.assertEqual(get_srv[0].status.name, "StatusTwo")
        self.assertEqual(get_srv[0].type.name, "TypeTwo")
        self.assertEqual(get_srv[0].ips, [ips_two])
        self.assertEqual(get_srv[0].tags, [tag_two])
        self.assertEqual(get_srv[0].admins, [admin_two])

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
