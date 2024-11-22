from django.urls import path
from .views import *
#app_name = 'comicsmxapi'

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    # Whatsapp routtes
    path('wa-templates/', WaMessageTemplatesView.as_view()), 
    path('wa-send-multiple-numbers-message', WaSendMultipleNumberMessageView.as_view(), name='send-customer-notification'), 
    #providers
    path('ship-providers', ShipProvidersView.as_view()),
    #webhooks
    path('mercado-libre/sync-account', MecadoLibreSyncView.as_view()),
    path('mercado-libre/webhook', WebhookMeli.as_view()),
    path('walmart/webhook', WalmartWebhook.as_view()),
    path('woocommerce/webhook', WoocommerceWebhook.as_view()),
    #customers
    path('customers', CustomersView.as_view()),
    #orders
    path('orders', OrderView.as_view())
]
