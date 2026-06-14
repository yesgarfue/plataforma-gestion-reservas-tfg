from django.urls import path

app_name = 'reservations'

urlpatterns = [
    path('paso1/', lambda r: None, name='step1'),
    path('paso2/', lambda r: None, name='step2'),
    path('paso3/', lambda r: None, name='step3'),
    path('confirmacion/', lambda r: None, name='confirmation'),
    path('cancelar/<str:codigo>/', lambda r: None, name='cancel'),
    path('seguimiento/', lambda r: None, name='tracking'),
    path('seguimiento/<str:codigo>/', lambda r: None, name='tracking_detail'),
    path('mis-reservas/', lambda r: None, name='my_reservations'),
]
