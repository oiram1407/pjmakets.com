from django.db import models
from django.contrib.auth.models import User
from .constants import constants

class Companie(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    status = models.CharField(max_length=50, choices=constants.Statuses, default="Active")
    date_published = models.DateTimeField(auto_now_add=True, verbose_name = "date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name = "date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class CompaniesUserRelated(models.Model):
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    user_company = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "user_company")
    status = models.CharField(max_length=50, choices=constants.Statuses, default="Active")
    date_published = models.DateTimeField(auto_now_add=True, verbose_name = "date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name = "date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class CompaniesPlataformsRelated(models.Model):
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    plataform = models.CharField(max_length=250, choices=constants.Plataforms)
    data = models.TextField(max_length = 10000, blank=False)
    status = models.CharField(max_length=50, choices=constants.Statuses, default="Active")
    date_published = models.DateTimeField(auto_now_add=True, verbose_name = "date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name = "date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

