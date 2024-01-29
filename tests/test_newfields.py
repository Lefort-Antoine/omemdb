import unittest

from tests.app_newfields import AppNewFields
class TestNewFields(unittest.TestCase):
    def test_custom_fields(self):
        db = AppNewFields()
        db.ref_field_record(ref="name_1")
        db.ref_field_record2(ref="other_1")
        # use TupleLinkField
        db.custom_fields_record.add(
            pk=0,
            tuple=(1,2,3),
            tuple_link=("name_1", "other_1"),
            augmented_field="my augmented field"
        )
        # save and load "augmented field" in/to json data


        # batch modify "augmented field" (description, metadata)
        # https://stackoverflow.com/questions/70259387/how-to-batch-modify-metadata-arguments-in-field-due-to-removedinmarshmallow4wa
