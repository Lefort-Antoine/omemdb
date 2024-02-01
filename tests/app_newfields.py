from omemdb.packages.omarsh import Schema as MarshSchema, fields
from omemdb import Record, Db, TupleLinkField

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class RefFieldRecord(Record):
    class Schema(MarshSchema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass

class RefFieldRecord2(Record):
    class Schema(MarshSchema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass

class CustomFieldsRecord(Record):
    class Schema(MarshSchema):
        pk = fields.RefField(required=True)
        tuple_of_int = fields.Tuple(
            (fields.Integer(), fields.Integer(), fields.Integer()),
            required=True,
        )
        # FIXME: does not work if specified, works with None as default
        tuple_of_nested = fields.Tuple(
            (
                fields.Nested(RefFieldRecord.Schema()),
                fields.Nested(RefFieldRecord2.Schema()),
            ),
            required=False,
            load_default=None,
        )
        list_of_type = fields.List(
            fields.Nested(RefFieldRecord.Schema()), allow_none=True, load_default=None
        )
        dict_of_nested = fields.Dict(
            keys=fields.Str(),
            values=fields.Nested(RefFieldRecord.Schema()),
            allow_none=True,
            load_default=None,
        )

        # TODO: finish this and add into JSON export
        # https://github.com/lovasoa/marshmallow_dataclass/issues/119
        augmented_field = fields.String(
            metadata=dict(
                unit="m2",
                description="This is a decription of the field.",
            ),
            allow_none=True,
            load_default=None,
        )
    class TableMeta:
        pass

class AppNewFields(Db):
    models = [
        CustomFieldsRecord,
        RefFieldRecord,
        RefFieldRecord2
    ]
