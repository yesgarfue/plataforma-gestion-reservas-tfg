from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('barcos/', views.BarcoListView.as_view(), name='barco_list'),
    path('barcos/<int:id>/', views.BarcoDetailView.as_view(), name='barco_detail'),
]
