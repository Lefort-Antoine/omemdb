import unittest

from tests.app_newfields import AppNewFields
class TestNewFields(unittest.TestCase):
    def test_custom_fields(self):
        db = AppNewFields()

        rec1 = db.ref_field_record.add(
            ref="Rec1",
        )
        # rec1_bis = db.ref_field_record.add(
        #     ref="Rec1_bis",
        # )
        rec2 = db.ref_field_record.add(
            ref="Rec2",
        )

        db.custom_fields_record.add(
            pk=0,
            tuple_of_int=(1,2,3),
            tuple_of_nested=(rec1, rec2),
            # list_of_type=(rec1, rec1_bis ),
            augmented_field="my augmented field"
        )
        # save and load "augmented field" in/to json data


        # batch modify "augmented field" (description, metadata)
        # https://stackoverflow.com/questions/70259387/how-to-batch-modify-metadata-arguments-in-field-due-to-removedinmarshmallow4wa
