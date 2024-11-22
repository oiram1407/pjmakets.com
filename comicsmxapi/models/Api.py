from django.db import models
from django.contrib.auth.models import User
from .constants import constants

class ApiLog(models.Model):
    origin = models.CharField(max_length=300, null=False, default=None)
    url = models.CharField(max_length=500, null=False, blank=True)
    method = models.CharField(max_length=100, null=False, blank=True)
    headers = models.TextField(max_length=100000, null=False)
    body = models.TextField(max_length=100000, null=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    