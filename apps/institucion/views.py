from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from .models import Institucion, ContactoMensaje

def pagina_inicio(request):
    institucion = Institucion.objects.first() 
    return render(request, 'institucion/inicio.html', {'institucion': institucion})

def pagina_nosotros(request):
    institucion = Institucion.objects.first() 
    return render(request, 'institucion/nosotros.html', {'institucion': institucion})

def pagina_contacto(request):
    institucion = Institucion.objects.first()
    
    if request.method == 'POST':
        # Recuperar datos del formulario
        nombre = request.POST.get('name')
        correo = request.POST.get('email')
        telefono = request.POST.get('phone')
        asunto = request.POST.get('subject')
        mensaje = request.POST.get('message')
        
        try:
            # Guardar en la base de datos
            ContactoMensaje.objects.create(
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                asunto=asunto,
                mensaje=mensaje
            )
            
            # Enviar correo electrónico
            enviar_correo_contacto(nombre, correo, telefono, asunto, mensaje)
            
            messages.success(request, '¡Mensaje enviado correctamente! Nos pondremos en contacto contigo en breve.')
            return redirect('contacto')
        
        except Exception as e:
            messages.error(request, f'Error al enviar el mensaje: {str(e)}')
    
    return render(request, 'institucion/contacto.html', {'institucion': institucion})

def enviar_correo_contacto(nombre, correo, telefono, asunto, mensaje):
    # Configurar el correo de destino
    correo_destino = 'clopez6341@uta.edu.ec'
    
    # Crear el contexto para la plantilla de correo
    context = {
        'nombre': nombre,
        'correo': correo,
        'telefono': telefono if telefono else 'No proporcionado',
        'asunto': asunto,
        'mensaje': mensaje,
        'fecha': timezone.now().strftime("%d/%m/%Y %H:%M")
    }
    
    # Renderizar la plantilla de correo HTML
    html_content = render_to_string('institucion/email/contacto_email.html', context)
    
    # Crear versión de texto plano
    text_content = strip_tags(html_content)
    
    # Crear el correo
    email = EmailMultiAlternatives(
        f'Nuevo mensaje de contacto: {asunto}',
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [correo_destino]
    )
    
    # Adjuntar contenido HTML
    email.attach_alternative(html_content, "text/html")
    
    # Enviar el correo
    email.send()
