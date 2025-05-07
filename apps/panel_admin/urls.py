from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    path('configuracion/', views.configuracion_sitio, name='configuracion_sitio'),
    path('configuracion/logo/', views.guardar_logo, name='guardar_logo'),
    path('configuracion/favicon/', views.guardar_favicon, name='guardar_favicon'),
    path('configuracion/logo_web/', views.cambiar_logo_web, name='configurar_logo_web'),
    path('configuracion/info-sitio/', views.guardar_info_sitio, name='guardar_info_sitio'),
    path('configuracion/contacto/', views.guardar_contacto, name='guardar_contacto'),
    path('configuracion/redes-sociales/', views.guardar_redes_sociales, name='guardar_redes_sociales'),
    path('configuracion/info-legal/', views.guardar_info_legal, name='guardar_info_legal'),
    path('configuracion/guardar-todo/', views.guardar_todo, name='guardar_todo'),

    path('tasas/', views.modificar_tasas, name='modificar_tasas'),

    path('admin/usuarios/', views.administrar_usuarios, name='administrar_usuarios'),
    path('admin/usuarios/detalle/<int:usuario_id>/', views.detalle_usuario, name='detalle_usuario'),
    path('admin/usuarios/crear-cliente/', views.crear_cliente, name='crear_cliente'),
    path('admin/usuarios/crear-admin/', views.crear_admin, name='crear_admin'),
    path('admin/usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('admin/usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    path('admin/inversiones/', views.administrar_inversiones, name='administrar_inversiones'),
    path('admin/inversiones/nuevo/', views.crear_tipo_inversion, name='crear_tipo_inversion'),
    path('admin/inversiones/<int:inversion_id>/', views.detalle_tipo_inversion, name='detalle_tipo_inversion'),
    path('admin/inversiones/<int:inversion_id>/editar/', views.editar_tipo_inversion, name='editar_tipo_inversion'),
    path('admin/inversiones/<int:inversion_id>/eliminar/', views.eliminar_tipo_inversion, name='eliminar_tipo_inversion'),

    path('admin/creditos/', views.administrar_creditos, name='administrar_creditos'),
    path('admin/creditos/detalle/<int:credito_id>/', views.detalle_tipo_credito, name='detalle_tipo_credito'),
    path('admin/creditos/crear/', views.crear_tipo_credito, name='crear_tipo_credito'),
    path('admin/creditos/editar/<int:credito_id>/', views.editar_tipo_credito, name='editar_tipo_credito'),
    path('admin/creditos/eliminar/<int:credito_id>/', views.eliminar_tipo_credito, name='eliminar_tipo_credito'),

    # URLs para la gestión de reportes
    path('admin/reportes/', views.administrar_reportes, name='administrar_reportes'),
    path('admin/reportes/inversion/<int:inversion_id>/', views.detalle_reporte_inversion, name='detalle_reporte_inversion'),
    path('admin/reportes/credito/<int:credito_id>/', views.detalle_reporte_credito, name='detalle_reporte_credito'),
]