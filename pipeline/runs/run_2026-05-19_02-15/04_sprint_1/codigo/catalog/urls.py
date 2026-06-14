from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.BarcoListView.as_view(), name='barco_list'),
    path('<int:id>/', views.BarcoDetailView.as_view(), name='barco_detail'),
]
