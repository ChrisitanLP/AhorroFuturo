from django.shortcuts import render

def dashboard(request):
    return render(request, 'panel_admin/dashboard.html')

def configurar_logo(request):
    return render(request, 'panel_admin/configurar_logo.html')

def modificar_tasas(request):
    return render(request, 'panel_admin/modificar_tasas.html')

def administrar_creditos(request):
    return render(request, 'panel_admin/administrar_creditos.html')