from django.db import models
from django.contrib.auth.models import User
from .Companies import Companie
from .constants import constants

class Product(models.Model):
	name = models.CharField(max_length=250, null=False)
	sku = models.CharField(max_length=500, unique=True, null=False)
	status = models.CharField(max_length=100, default="Active", choices=constants.Statuses)
	company = models.ForeignKey(Companie, on_delete=models.CASCADE)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class ProductMeta(models.Model):
	product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
	description = models.TextField(max_length=10000, null=True, blank=True)
	images = models.TextField(max_length=10000, null=True, blank=True)
	weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
	height = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	width = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	length = models.DecimalField(max_digits=10, decimal_places=2, null=True)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class ProductsPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    plataform_name = models.CharField(max_length=100, choices=constants.Plataforms)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class ProductsRelatedPlataform(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_plataform_id = models.CharField(max_length=250, null=False)
	method = models.CharField(max_length=100, choices=constants.Plataforms)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class ProductsInventory(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0, null=False)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class ProductsInventoryUpdate(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0, null=False)
	method_update = models.CharField(max_length=100, choices=constants.Plataforms)
	action_type = models.CharField(max_length=100, choices=constants.ActionInventyory, default="increment")
	status = models.CharField(max_length=100, null=False, blank=False, choices=constants.Statuses, default='Inactive')
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

class ProductUpdatedLog(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	method = models.CharField(max_length=100, choices=constants.Plataforms)
	action = models.TextField(max_length = 1000, blank=False)
	action_type = models.CharField(max_length=100, choices=constants.ActionInventyory, default="increment")
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

	
