from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('paso1/', views.ReservationStep1View.as_view(), name='step1'),
    path('paso2/', views.ReservationStep2View.as_view(), name='step2'),
    path('paso3/', views.ReservationStep3View.as_view(), name='step3'),
    path('confirmacion/', views.ReservationConfirmationView.as_view(), name='confirmation'),
    path('cancelar/<str:codigo>/', views.CancelReservationView.as_view(), name='cancel'),
    path('seguimiento/', views.TrackingView.as_view(), name='tracking'),
    path('seguimiento/<str:codigo>/', views.TrackingDetailView.as_view(), name='tracking_detail'),
    path('mis-reservas/', views.MyReservationsView.as_view(), name='my_reservations'),
]
