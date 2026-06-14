from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('cesta/', views.CartView.as_view(), name='cart'),
    path('cesta/agregar/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cesta/actualizar/', views.UpdateCartView.as_view(), name='update_cart'),
    path('cesta/vaciar/', views.ClearCartView.as_view(), name='clear_cart'),
    path('reserva/paso1/', views.ReservationStep1View.as_view(), name='step1'),
    path('reserva/paso2/', views.ReservationStep2View.as_view(), name='step2'),
    path('reserva/paso3/', views.ReservationStep3View.as_view(), name='step3'),
    path('reserva/confirmacion/', views.ConfirmationView.as_view(), name='confirmation'),
    path('reserva/cancelar/<str:codigo>/', views.CancelReservationView.as_view(), name='cancel'),
]
