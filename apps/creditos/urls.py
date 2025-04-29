from django.urls import path
from . import views

urlpatterns = [
    path('simulador/', views.simulador_credito, name='simulador_credito'),
    path('calcular/', views.calcular_credito, name='calcular'),
]