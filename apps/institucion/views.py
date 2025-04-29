from django.shortcuts import render
from .models import Institucion

def pagina_inicio(request):
    institucion = Institucion.objects.first() 
    return render(request, 'institucion/inicio.html', {'institucion': institucion})

def pagina_nosotros(request):
    institucion = Institucion.objects.first() 
    return render(request, 'institucion/nosotros.html', {'institucion': institucion})

def pagina_contacto(request):
    institucion = Institucion.objects.first() 
    return render(request, 'institucion/contacto.html', {'institucion': institucion})



