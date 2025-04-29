from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.institucion.urls')),
    path('auth/', include('apps.autenticacion.urls')),
    path('institucion/', include('apps.institucion.urls')),
    path('creditos/', include('apps.creditos.urls')),
    path('inversiones/', include('apps.inversiones.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
