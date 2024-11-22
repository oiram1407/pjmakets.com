from django.db import models
from django.contrib.auth.models import User
from .constants import constants

class ShipProviders(models.Model):
    provider_name = models.CharField(max_length=250,null=False)
    provider_slug = models.CharField(max_length=250,null=False)
    provider_url = models.CharField(max_length=250,null=False)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    status = models.CharField(max_length=100, default="Active", choices=constants.Statuses)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

class Shiplog(models.Model):
    pass