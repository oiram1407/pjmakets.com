from django.db import models
from django.contrib.auth.models import User
from .constants import constants

class WaMessagesTemplates(models.Model):
    template_name = models.CharField(max_length=150, null=False)
    message = models.TextField(max_length=5000, null=False, blank=True)
    status = models.CharField(max_length=150, default='Active', choices=constants.Statuses)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    def __str__(self):
        return self.template_name

class WaOutCommingLog(models.Model):
	to_number = models.CharField(max_length=15, null=False)
	template = models.ForeignKey(WaMessagesTemplates, on_delete=models.DO_NOTHING)
	params_sent = models.TextField(max_length=1000,null=False)
	message_sid = models.CharField(max_length=350, null=False)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	
class WaOutcomigProgramedMessages(models.Model):
	to_numbers = models.TextField(max_length=1000, null=False)
	template = models.ForeignKey(WaMessagesTemplates, on_delete=models.DO_NOTHING)
	params_sent = models.TextField(max_length=1000,null=False)
	date_time_to_send = models.DateTimeField(auto_now=False)
	date_published = models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
	user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
