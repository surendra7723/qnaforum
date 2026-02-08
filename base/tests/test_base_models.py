from django.test import TestCase
from base.models.base import TimedBaseModel
from django.db import models

class DummyModel(TimedBaseModel):
    name = models.CharField(max_length=10)
    class Meta:
        app_label = 'base'

class TimedBaseModelTest(TestCase):
    def test_created_and_modified_fields(self):
        obj = DummyModel.objects.create(name='test')
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.modified_at)
        # On save, modified_at should update
        old_modified = obj.modified_at
        obj.name = 'changed'
        obj.save()
        self.assertNotEqual(obj.modified_at, old_modified)
