from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('paso1/', views.ReservationStep1View.as_view(), name='step1'),
    path('paso2/', views.ReservationStep2View.as_view(), name='step2'),
    path('paso3/', views.ReservationStep3View.as_view(), name='step3'),
    path('confirmacion/', views.ReservationConfirmationView.as_view(), name='confirmation'),
    path('seguimiento/', views.TrackReservationView.as_view(), name='track'),
    path('mis-reservas/', views.MyReservationsView.as_view(), name='my_reservations'),
    path('<int:id>/cancelar/', views.CancelReservationView.as_view(), name='cancel'),
    path('paypal/return/', views.PayPalReturnView.as_view(), name='paypal_return'),
    path('paypal/cancel/', views.PayPalCancelView.as_view(), name='paypal_cancel'),
]
