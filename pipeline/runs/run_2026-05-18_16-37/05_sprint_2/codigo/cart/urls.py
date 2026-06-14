from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='view'),
    path('agregar/', views.AddToCartView.as_view(), name='add'),
    path('actualizar/', views.UpdateCartView.as_view(), name='update'),
    path('vaciar/', views.ClearCartView.as_view(), name='clear'),
]
