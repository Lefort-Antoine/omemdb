from omemdb.packages.omarsh import Schema as MarshSchema, fields
from omemdb import Record, Db


class CustomFieldsRecord(Record):
    class Schema(MarshSchema):
        pk = fields.Int(required=True)
        date_time = fields.DateTime(allow_none=True, load_default=None)
        date = fields.Date(allow_none=True, load_default=None)
        time = fields.Time(allow_none=True, load_default=None)
        time_delta = fields.TimeDelta(allow_none=True, load_default=None)
        numpy_array = fields.NumpyArray(allow_none=True, load_default=None)

    class TableMeta:
        pass


class RefFieldRecord(Record):
    class Schema(MarshSchema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass


class AllowNoneFieldRecord(Record):
    """
    allow_none documentation:
    Set this to True if None should be considered a valid value during validation/deserialization.
    If load_default=None and allow_none is unset, will default to True. Otherwise, the default is False.
    """
    class Schema(MarshSchema):
        ref = fields.RefField(required=True)
        can_be_none = fields.Int(allow_none=True, load_default=None)
        cant_be_none = fields.Int(allow_none=False, load_default=0)
        default_can_be_none = fields.Int(allow_none=True, load_default=None)
        default_cant_be_none = fields.Int(load_default=0)


class AppFields(Db):
    models = [
        CustomFieldsRecord,
        RefFieldRecord,
        AllowNoneFieldRecord
    ]
