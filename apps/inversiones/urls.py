from django.urls import path
from . import views

urlpatterns = [
    path('simulador-inversion/', views.simulador_inversion, name='simulador_inversion'),
    path('api/calcular-inversion/', views.calcular_inversion, name='calcular_inversion'),
    path('api/tipo-inversion/<int:tipo_id>/', views.obtener_datos_tipo_inversion, name='api_tipo_inversion'),
]