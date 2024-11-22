from django.db import models
from django.contrib.auth.models import User
from .constants import constants
from .Whatsapp import WaMessagesTemplates
from .Order import OrderPlataformRelated
from .Companies import Companie

class Customer(models.Model):
    first_name = models.CharField(max_length=250, null=False, blank=False)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    company = models.ForeignKey(Companie, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=100, default="Active", choices=constants.Statuses)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

class CustomerNotifications(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, null=False)
    template = models.ForeignKey(WaMessagesTemplates, on_delete=models.DO_NOTHING, null=False)
    data = models.TextField(max_length=10000, blank=False, null=True)
    type_notification = models.CharField(max_length=100, null=False, blank=False, default="order_recived", choices=constants.Type_notificatioon)
    status = models.CharField(max_length=100, default="pedding", choices=constants.Statuses_notifications)
    order = models.ForeignKey(OrderPlataformRelated, on_delete=models.DO_NOTHING, null=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
