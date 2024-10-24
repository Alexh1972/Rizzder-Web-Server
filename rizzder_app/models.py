from django.db import models


class TestEntity(models.Model):
    testColumn = models.CharField(max_length=200)
