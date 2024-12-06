from django.db import models
from django.contrib.auth.models import User
from .Companies import Companie
from .constants import constants

class CategoriesRelated(models.Model):
    method = models.CharField(max_length=250, choices=constants.Plataforms)
    category_id = models.TextField(max_length=250, null=True, blank=True)
    category_related_id = models.TextField(max_length=250, null=True, blank=True)
    method_related = models.CharField(max_length=250, choices=constants.Plataforms)
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "comicsmxapi_categories_related"

class CategoriesRelatedAttributes(models.Model):
    pass