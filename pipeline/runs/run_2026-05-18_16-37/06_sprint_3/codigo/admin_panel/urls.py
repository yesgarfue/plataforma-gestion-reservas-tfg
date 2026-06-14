from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('barcos/', views.AdminBoatsListView.as_view(), name='boats_list'),
    path('barcos/crear/', views.AdminBoatsCreateView.as_view(), name='boats_create'),
    path('barcos/<int:id>/editar/', views.AdminBoatsEditView.as_view(), name='boats_edit'),
    path('barcos/<int:id>/eliminar/', views.AdminBoatsDeleteView.as_view(), name='boats_delete'),
    path('clientes/', views.AdminClientsListView.as_view(), name='clients_list'),
    path('clientes/<int:id>/eliminar/', views.AdminClientsDeleteView.as_view(), name='clients_delete'),
    path('reservas/', views.AdminReservationsListView.as_view(), name='reservations_list'),
    path('reservas/<int:id>/', views.AdminReservationsDetailView.as_view(), name='reservations_detail'),
    path('reservas/<int:id>/cambiar-estado/', views.AdminReservationsChangeStateView.as_view(), name='reservations_change_state'),
]
