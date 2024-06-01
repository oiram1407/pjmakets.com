from django.db import models
from django.contrib.auth.models import User
from .constants import constants
from .Companies import Companie

class OrderPlataformRelated(models.Model):
    company = models.ForeignKey(Companie, on_delete=models.CASCADE)
    plataform = models.CharField(max_length=250, choices=constants.Plataforms)
    order_plataform_id = models.CharField(max_length=500, unique=True, blank=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    data = models.TextField(max_length = 10000, blank=False)
    status = models.CharField(max_length=50, choices=constants.Statuses_orders, default="pending")
    date_order = models.DateTimeField(verbose_name="date order", null=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name = "date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name = "date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)