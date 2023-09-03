from django.test import TestCase

from store.models import Tag


class TagTestCase(TestCase):
    def test_str_should_return_name(self):
        name = 'xyz'
        tag = Tag(name=name)
        self.assertEqual(str(tag), name)
