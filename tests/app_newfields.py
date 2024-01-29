from omemdb.packages.omarsh import Schema, fields
from omemdb import Record, Db, TupleLinkField

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class CustomFieldsRecord(Record):
    class Schema(Schema):
        pk = fields.RefField(required=True)
        tuple = fields.Tuple((fields.Integer(),fields.Integer(),fields.Integer()), allow_none=True, load_default=None)
        tuple_link = TupleLinkField(("RefFieldRecord", "RefFieldRecord2"), allow_none=True, load_default=None)
        augmented_field = fields.String(
            description="This is a decription of the field.",
            metadata=dict(unit="m2")
        )
    class TableMeta:
        pass

class RefFieldRecord(Record):
    class Schema(Schema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass


class RefFieldRecord2(Record):
    class Schema(Schema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass

class AppNewFields(Db):
    models = [
        CustomFieldsRecord,
        RefFieldRecord,
        RefFieldRecord2
    ]
