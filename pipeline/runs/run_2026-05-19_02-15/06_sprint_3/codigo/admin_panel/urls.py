from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('barcos/', views.AdminBoatsListView.as_view(), name='boats_list'),
    path('barcos/crear/', views.AdminBoatCreateView.as_view(), name='boat_create'),
    path('barcos/<int:id>/editar/', views.AdminBoatEditView.as_view(), name='boat_edit'),
    path('barcos/<int:id>/eliminar/', views.AdminBoatDeleteView.as_view(), name='boat_delete'),
    path('clientes/', views.AdminClientsListView.as_view(), name='clients_list'),
    path('clientes/<int:id>/eliminar/', views.AdminClientDeleteView.as_view(), name='client_delete'),
    path('reservas/', views.AdminReservationsListView.as_view(), name='reservations_list'),
    path('reservas/<int:id>/', views.AdminReservationDetailView.as_view(), name='reservation_detail'),
    path('reservas/<int:id>/cambiar-estado/', views.AdminReservationChangeStateView.as_view(), name='reservation_change_state'),
]
