from pytest import mark

from tests.integration.helpers.asserts import Asserts
from tests.integration.helpers.fixtures import refresh_db_before

from app import run
from app.db.models.tag import Tag
from app.db.operations.basic.tag import TagOp


@mark.db_operations
@mark.op_tag
class TestTagOp(Asserts):
    """ Integration tests for TagOp class.
        Operations on Tag model.
    """

    def case_add_records(self, refresh_db_before):
        """ Add new records to Tag table."""
        new_names = ["tag1", "tag2", "tag3"]

        for name in new_names:
            TagOp.add(name)

        check_records = TagOp.get()

        self.assertEqual(len(check_records), len(new_names))

        for record, exp_name in zip(check_records, new_names):
            self.assertTrue(isinstance(record, Tag))
            self.assertEqual(record.name, exp_name)

    def case_get_by_id(self, refresh_db_before):
        """ Create test records in Tag table and get them by id."""
        names_with_id = {"tag1": 1, "tag2": 2, "tag3": 3}

        for name in names_with_id.keys():
            TagOp.add(name)

        for exp_name, exp_id in names_with_id.items():
            tag_obj = TagOp.get(id=exp_id)
            self.assertTrue(len(tag_obj) is 1)
            self.assertEqual(exp_name, tag_obj[0].name)
            self.assertEqual(exp_id, tag_obj[0].id)

    def case_get_by_name_one_result(self, refresh_db_before):
        """ Create test records in Tag table and get them by name."""
        names_with_id = {"tag1": 1, "tag2": 2, "tag3": 3}

        for name in names_with_id.keys():
            TagOp.add(name)

        for exp_name, exp_id in names_with_id.items():
            tag_obj = TagOp.get(name=exp_name)
            self.assertTrue(len(tag_obj) is 1)
            self.assertEqual(exp_name, tag_obj[0].name)
            self.assertEqual(exp_id, tag_obj[0].id)

    def case_update_record(self, refresh_db_before):
        """ Create test record in Tag table and then update it."""
        original_name = "tag3"
        update_name = "tag33"

        original_tag = TagOp.add(original_name)

        updated_tag_local = TagOp.update(original_tag, update_name)

        self.assertEqual(updated_tag_local.name, update_name)

        updated_tag_get = TagOp.get(name=update_name)

        self.assertTrue(len(updated_tag_get) is 1)
        self.assertEqual(updated_tag_get[0].name, update_name)
        self.assertEqual(updated_tag_get[0].id, original_tag.id)

    def case_delete_records(self, refresh_db_before):
        """ Create new record in Tag table and then delete it."""
        new_name = "tag1"

        TagOp.add(new_name)

        tag_obj = TagOp.get(name=new_name)
        self.assertTrue(len(tag_obj) is 1)
        self.assertEqual(tag_obj[0].name, new_name)

        TagOp.delete(tag_obj[0])

        tag_obj = TagOp.get(name=new_name)
        self.assertFalse(tag_obj)
