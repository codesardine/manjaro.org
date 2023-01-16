from django.db import models


class SearchLastUpdate(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(max_length=30)


class SearchData(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=160)
    is_doc = models.BooleanField(default=False)
    type = models.CharField(max_length=20)
    message = models.CharField(max_length=20)
    state = models.CharField(max_length=20, blank=True, null=True)