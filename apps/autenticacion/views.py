from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages

from .forms import LoginForm, RegistroClienteForm, RegistroAdminForm
from .models import Usuario

class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'autenticacion/login.html'
    
    def get_success_url(self):
        # Redireccionar según el tipo de usuario
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('dashboard')
        else:
            return reverse_lazy('inicio')

@login_required
def dashboard(request):
    # Vista que redirecciona según el tipo de usuario
    if request.user.is_superuser:
        return redirect('dashboard')
    else:
        return redirect('inicio')

@login_required
def admin_dashboard(request):
    # Verificar que solo admins puedan acceder
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta sección")
        return redirect('inicio')
    
    return render(request, 'autenticacion/admin_dashboard.html')

@login_required
def client_dashboard(request):
    # Verificar que solo clientes puedan acceder
    if not request.user.es_cliente():
        messages.error(request, "No tienes permisos para acceder a esta sección")
        return redirect('inicio')
    
    return render(request, 'autenticacion/client_dashboard.html')

class RegistroClienteView(CreateView):
    model = Usuario
    form_class = RegistroClienteForm
    template_name = 'autenticacion/registro_cliente.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request, "Registro exitoso. Ahora puedes iniciar sesión.")
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class RegistroAdminView(CreateView):
    model = Usuario
    form_class = RegistroAdminForm
    template_name = 'autenticacion/registro_admin.html'
    success_url = reverse_lazy('admin_dashboard')
    
    def dispatch(self, request, *args, **kwargs):
        # Solo los administradores pueden crear otros administradores
        if not request.user.es_admin():
            messages.error(request, "No tienes permisos para crear administradores")
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, "Administrador registrado exitosamente")
        return super().form_valid(form)
    
class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)