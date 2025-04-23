from django.db import models


class TimedBaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)


