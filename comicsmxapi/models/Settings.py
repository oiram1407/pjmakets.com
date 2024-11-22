from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Settings(models.Model):
	variable_name = models.CharField(max_length=250, null=False)
	variable_value = models.TextField(max_length=10000, null=False, blank=True)
	def __str__(self):
		return self.variable_name
