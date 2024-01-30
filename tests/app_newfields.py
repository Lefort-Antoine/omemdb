from omemdb.packages.omarsh import Schema, fields
from omemdb import Record, Db, TupleLinkField

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

class RefFieldRecord(Record):
    class Schema(Schema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass

# Why is this exactly the same?
class RefFieldRecord2(Record):
    class Schema(Schema):
        ref = fields.RefField(required=True)

    class TableMeta:
        pass

class CustomFieldsRecord(Record):
    class Schema(Schema):
        fields.RefField(required=True)
        fields.Tuple((fields.Integer(),fields.Integer(),fields.Integer()), allow_none=True, load_default=None)
        fields.Tuple((fields.Nested(RefFieldRecord), fields.Nested(RefFieldRecord2)), allow_none=False, load_default=None)

        # TODO: finish this and add into JSON export
        # https://github.com/lovasoa/marshmallow_dataclass/issues/119
        augmented_field = fields.String(
            metadata=dict(unit="m2", description="This is a decription of the field.",)
        )
    class TableMeta:
        pass

class AppNewFields(Db):
    models = [
        CustomFieldsRecord,
        RefFieldRecord,
        RefFieldRecord2
    ]
