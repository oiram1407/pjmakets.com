from ..models.Whatsapp import WaMessagesTemplates
from ..models.Customer import CustomerNotifications
import json

class NotificationsWhatsapp:
    def __init__(self) -> None:
        pass

    def getIDTemplateByName(self, _template_name):
        whatsapp_template = WaMessagesTemplates.objects.get(template_name=_template_name)

        return whatsapp_template.pk
