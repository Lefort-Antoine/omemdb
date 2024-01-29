from omemdb.packages.omarsh import Schema, fields
from omemdb import Record, Db, TupleLinkField

# https://marshmallow.readthedocs.io/en/stable/nesting.html

class User(Record):
    class Schema(Schema):
        name = fields.String()
        email = fields.Email()
        created_at = fields.DateTime()

class Blog(Record):
    class Schema(Schema):
        title = fields.String()
        author = fields.Nested(User)



class BookDb(Db):
    models = [
        User,
        Blog,
    ]