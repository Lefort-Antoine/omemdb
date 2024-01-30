from omemdb.packages.omarsh import Schema, fields
from omemdb import Record, Db, TupleLinkField

# https://marshmallow.readthedocs.io/en/stable/nesting.html

class User(Record):
    class Schema(Schema):
        pk = fields.RefField(required=True)
        name = fields.String(required=True)
        email = fields.Email(load_default=None, allow_none=True)
        created_at = fields.DateTime(load_default=None, allow_none=True)

class Blog(Record):
    class Schema(Schema):
        pk = fields.RefField(required=True)
        title = fields.String(required=True)
        author = fields.Nested(User.Schema, load_default=None, allow_none=True)

class BookDb(Db):
    models = [
        User,
        Blog,
    ]
