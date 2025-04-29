from django.urls import path
from .views import pagina_inicio
from .views import pagina_nosotros
from .views import pagina_contacto

urlpatterns = [
    path('', pagina_inicio, name='inicio'),
    path('nosotros/', pagina_nosotros, name='nosotros'),
    path('contacto/', pagina_contacto, name='contacto'),
]
