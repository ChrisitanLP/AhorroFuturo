from django.urls import path
from .views import CustomLogoutView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('registro/', views.RegistroClienteView.as_view(), name='registro_cliente'),
    path('registro/admin/', views.RegistroAdminView.as_view(), name='registro_admin'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
]