from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('paypal/', views.PayPalRedirectView.as_view(), name='paypal_redirect'),
    path('paypal/return/', views.PayPalReturnView.as_view(), name='paypal_return'),
    path('paypal/cancel/', views.PayPalCancelView.as_view(), name='paypal_cancel'),
    path('contra-reembolso/', views.CashOnDeliveryView.as_view(), name='cash_on_delivery'),
]
