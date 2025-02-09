import unittest

from tests.app_nested_fields import BookDb
# https://marshmallow.readthedocs.io/en/stable/nesting.html

class TestNewFields(unittest.TestCase):
    def test_nested(self):
        db = BookDb()
        db.user.add(
            name="MrX",
            email="dot.com",
        )
        db.blog.add(
            title="Something Completely Different", author=db.user.one()
        )
        self.assertEqual(db.blog.one().author.name, db.user.one().name)