from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('logo/', views.cambiar_logo, name='configurar_logo'),
    path('tasas/', views.modificar_tasas, name='modificar_tasas'),
    path('creditos/', views.administrar_creditos, name='administrar_creditos'),
]