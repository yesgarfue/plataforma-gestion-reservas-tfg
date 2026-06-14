from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('seguimiento/', views.TrackingSearchView.as_view(), name='search'),
    path('seguimiento/<str:codigo>/', views.TrackingDetailView.as_view(), name='detail'),
    path('mis-reservas/', views.MyReservationsView.as_view(), name='my_reservations'),
]
