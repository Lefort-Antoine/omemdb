import unittest
import tempfile
import os

from omemdb import TableDefinitionError, RecordDoesNotExistError, \
    MultipleRecordsReturnedError
from omemdb.packages.oerrors import OExceptionCollection, ValidationError

from tests.app_simple import AppSimpleDb
from tests.app_err import AppErrDb
from tests.app_building import AppBuildingDb
from tests.app_dynamic_id import AppDynamicId


def building_standard_populate():
    db = AppBuildingDb()

    # populate
    for c_i in range(3):
        db.construction.add(ref=f"c{c_i}")

    # create zones (batch)
    db.zone.batch_add((dict(ref=f"z{z_i}") for z_i in range(3)))

    for z_i in range(3):
        # create surfaces
        for s_i in range(3):
            db.surface.add(
                ref=f"s{z_i}{s_i}",
                major_zone=f"z{z_i}",
                minor_zone=None if s_i == 2 else f"z{s_i+1}",
                constructions=[f"c{c_i}" for c_i in range(3)]
            )

    return db


class TestExcel(unittest.TestCase):

    def test_basics(self):
        db = building_standard_populate()
        from omemdb.excel import generate_input_form

        with tempfile.TemporaryDirectory() as dir_path:
            generate_input_form(db, os.path.join(dir_path, "dbform.xlsx"))

            #todo: json_data to excel form to obtain a filled form
            #todo: from excel to json_data to load a filled form

