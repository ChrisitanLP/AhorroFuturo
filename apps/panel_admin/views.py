from django.shortcuts import render, redirect
from .models import ConfiguracionGlobal
from .forms import LogoForm

def dashboard(request):
    return render(request, 'panel_admin/dashboard.html')

def configurar_logo(request):
    return render(request, 'panel_admin/configurar_logo.html')

def modificar_tasas(request):
    return render(request, 'panel_admin/modificar_tasas.html')

def administrar_creditos(request):
    return render(request, 'panel_admin/administrar_creditos.html')

def cambiar_logo(request):
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            return redirect('configurar_logo')
    else:
        form = LogoForm(instance=config)

    return render(request, 'panel_admin/configurar_logo.html', {'form': form, 'logo_actual': config.logo})