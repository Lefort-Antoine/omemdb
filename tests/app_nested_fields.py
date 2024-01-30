from omemdb.packages.omarsh import Schema, fields
from omemdb import Record, Db, TupleLinkField

# https://marshmallow.readthedocs.io/en/stable/nesting.html

class User(Record):
    class Schema(Schema):
        pk = fields.RefField(required=True)
        name = fields.String(load_default=None)
        email = fields.Email(load_default=None)
        created_at = fields.DateTime(load_default=None)

class Blog(Record):
    class Schema(Schema):
        pk = fields.RefField(required=True)
        title = fields.String(load_default=None)
        author = fields.Nested(User, load_default=None)



class BookDb(Db):
    models = [
        User,
        Blog,
    ]
