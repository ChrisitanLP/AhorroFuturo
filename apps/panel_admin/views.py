from django.shortcuts import render, redirect, get_object_or_404
from .models import ConfiguracionGlobal
from .forms import LogoForm
from django.http import JsonResponse
from .forms import (
    LogoForm, FaviconForm, InfoSitioForm, InfoContactoForm, 
    RedesSocialesForm, InformacionLegalForm, ConfiguracionGeneralForm
)
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from apps.autenticacion.models import Usuario
from apps.autenticacion.forms import RegistroAdminForm, RegistroClienteForm
from apps.inversiones.models import TipoInversion, Inversion
from apps.inversiones.forms import TipoInversionForm
from apps.creditos.models import TipoCredito, Credito
from apps.creditos.forms import TipoCreditoForm
from apps.institucion.models import ContactoMensaje
import logging

# Configurar el logger para depuración
logger = logging.getLogger(__name__)

def es_admin(user):
    """Verifica si el usuario es administrador."""
    return user.is_authenticated and (user.tipo_usuario == Usuario.ADMIN or user.is_superuser)

@login_required
@user_passes_test(es_admin)
def dashboard(request):
    """Vista del dashboard administrativo"""
    
    try:
        # Obtener datos para las tarjetas de estadísticas
        total_usuarios = Usuario.objects.filter(tipo_usuario='cliente').count()
        logger.debug(f"Total usuarios clientes: {total_usuarios}")
        
        total_creditos = Credito.objects.all().count()
        logger.debug(f"Total créditos: {total_creditos}")
        
        total_inversiones = Inversion.objects.all().count()
        logger.debug(f"Total inversiones: {total_inversiones}")
        
        mensajes_contacto = ContactoMensaje.objects.all().count()
        logger.debug(f"Total mensajes de contacto: {mensajes_contacto}")
        
        mensajes_no_leidos = ContactoMensaje.objects.filter(leido=False).count()
        logger.debug(f"Mensajes no leídos: {mensajes_no_leidos}")
        
        # Obtener datos para gráficos y actividad reciente
        fecha_limite = timezone.now() - timedelta(days=30)
        
        # Actividad reciente (últimos 30 días)
        mensajes_recientes = ContactoMensaje.objects.filter(
            fecha_creacion__gte=fecha_limite
        ).order_by('-fecha_creacion')[:3]
        logger.debug(f"Mensajes recientes (últimos 30 días): {mensajes_recientes.count()}")
        
        creditos_recientes = Credito.objects.filter(
            fecha_creacion__gte=fecha_limite
        ).order_by('-fecha_creacion')[:3]
        logger.debug(f"Créditos recientes (últimos 30 días): {creditos_recientes.count()}")
        
        inversiones_recientes = Inversion.objects.filter(
            fecha_creacion__gte=fecha_limite
        ).order_by('-fecha_creacion')[:3]
        logger.debug(f"Inversiones recientes (últimos 30 días): {inversiones_recientes.count()}")
        
        # Datos para gráficos
        mes_actual = timezone.now().month
        anio_actual = timezone.now().year
        
        creditos_mes_actual = Credito.objects.filter(
            fecha_creacion__month=mes_actual,
            fecha_creacion__year=anio_actual
        ).count()
        logger.debug(f"Créditos del mes actual: {creditos_mes_actual}")
        
        inversiones_mes_actual = Inversion.objects.filter(
            fecha_creacion__month=mes_actual,
            fecha_creacion__year=anio_actual
        ).count()
        logger.debug(f"Inversiones del mes actual: {inversiones_mes_actual}")
        
        context = {
            'total_usuarios': total_usuarios,
            'total_creditos': total_creditos,
            'total_inversiones': total_inversiones,
            'mensajes_contacto': mensajes_contacto,
            'mensajes_no_leidos': mensajes_no_leidos,
            'mensajes_recientes': mensajes_recientes,
            'creditos_recientes': creditos_recientes,
            'inversiones_recientes': inversiones_recientes,
            'creditos_mes_actual': creditos_mes_actual,
            'inversiones_mes_actual': inversiones_mes_actual,
        }
        
        return render(request, 'panel_admin/dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Error en el dashboard: {str(e)}")
        context = {
            'error_message': f"Ocurrió un error al cargar el dashboard: {str(e)}"
        }
        return render(request, 'panel_admin/dashboard.html', context)

@login_required
@user_passes_test(es_admin)
def configuracion_sitio(request):
    """Vista principal de configuración con pestañas para diferentes secciones"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()
    
    # Para cada sección, preparamos el formulario correspondiente
    logo_form = LogoForm(instance=config)
    favicon_form = FaviconForm(instance=config)
    info_sitio_form = InfoSitioForm(instance=config)
    info_contacto_form = InfoContactoForm(instance=config)
    redes_sociales_form = RedesSocialesForm(instance=config)
    info_legal_form = InformacionLegalForm(instance=config)
    
    # Determinamos qué pestaña está activa
    active_tab = request.GET.get('tab', 'general')
    
    context = {
        'config': config,
        'logo_form': logo_form,
        'favicon_form': favicon_form,
        'info_sitio_form': info_sitio_form,
        'info_contacto_form': info_contacto_form,
        'redes_sociales_form': redes_sociales_form,
        'info_legal_form': info_legal_form,
        'active_tab': active_tab
    }
    
    return render(request, 'panel_admin/configuracion.html', context)

@login_required
@user_passes_test(es_admin)
def guardar_logo(request):
    """Guardar logo del sitio"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Logo actualizado correctamente")
        else:
            messages.error(request, "Error al actualizar el logo")
    
    return redirect('configuracion_sitio')

@login_required
@user_passes_test(es_admin)
def guardar_favicon(request):
    """Guardar favicon del sitio"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = FaviconForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Favicon actualizado correctamente")
        else:
            messages.error(request, "Error al actualizar el favicon")
    
    return redirect('configuracion_sitio')

@login_required
@user_passes_test(es_admin)
def guardar_info_sitio(request):
    """Guardar información general del sitio"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = InfoSitioForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Información del sitio actualizada correctamente")
        else:
            messages.error(request, "Error al actualizar la información del sitio")
    
    return redirect('configuracion_sitio')

@login_required
@user_passes_test(es_admin)
def guardar_contacto(request):
    """Guardar información de contacto"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = InfoContactoForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Información de contacto actualizada correctamente")
        else:
            messages.error(request, "Error al actualizar la información de contacto")
    
    return redirect('configuracion_sitio')

@login_required
@user_passes_test(es_admin)
def guardar_redes_sociales(request):
    """Guardar enlaces de redes sociales"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = RedesSocialesForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Redes sociales actualizadas correctamente")
        else:
            messages.error(request, "Error al actualizar las redes sociales")
    
    return redirect('configuracion_sitio')

@login_required
@user_passes_test(es_admin)
def guardar_info_legal(request):
    """Guardar información legal"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = InformacionLegalForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Información legal actualizada correctamente")
        else:
            messages.error(request, "Error al actualizar la información legal")
    
    return redirect('configuracion_sitio')

@login_required
@user_passes_test(es_admin)
def guardar_todo(request):
    """Guardar toda la configuración en una única operación"""
    config = ConfiguracionGlobal.objects.first()
    if not config:
        config = ConfiguracionGlobal.objects.create()

    if request.method == 'POST':
        form = ConfiguracionGeneralForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuración actualizada correctamente")
            return JsonResponse({'status': 'success'})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'status': 'error', 'errors': errors})
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

def modificar_tasas(request):
    return render(request, 'panel_admin/modificar_tasas.html')

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

@login_required
@user_passes_test(es_admin)
def administrar_usuarios(request):
    """Vista para listar y gestionar usuarios."""
    clientes = Usuario.objects.filter(tipo_usuario=Usuario.CLIENTE)
    administradores = Usuario.objects.filter(tipo_usuario=Usuario.ADMIN)
    
    return render(request, 'panel_admin/gestor_usuarios.html', {
        'clientes': clientes,
        'administradores': administradores,
    })

@login_required
@user_passes_test(es_admin)
def detalle_usuario(request, usuario_id):
    """Vista para ver detalles de un usuario específico."""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    return render(request, 'panel_admin/gestion_usuarios/detalle_usuario.html', {
        'usuario': usuario,
    })

@login_required
@user_passes_test(es_admin)
def crear_cliente(request):
    """Vista para crear un nuevo cliente."""
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado exitosamente.')
            return redirect('administrar_usuarios')
    else:
        form = RegistroClienteForm()
    
    return render(request, 'panel_admin/gestion_usuarios/form_usuario.html', {
        'form': form,
        'titulo': 'Nuevo Cliente',
        'accion': 'Crear',
    })

@login_required
@user_passes_test(es_admin)
def crear_admin(request):
    """Vista para crear un nuevo administrador."""
    if request.method == 'POST':
        form = RegistroAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Administrador creado exitosamente.')
            return redirect('administrar_usuarios')
    else:
        form = RegistroAdminForm()
    
    return render(request, 'panel_admin/gestion_usuarios/form_usuario.html', {
        'form': form,
        'titulo': 'Nuevo Administrador',
        'accion': 'Crear',
    })

@login_required
@user_passes_test(es_admin)
def editar_usuario(request, usuario_id):
    """Vista para editar un usuario existente."""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Seleccionar el formulario correcto según el tipo de usuario
    if usuario.tipo_usuario == Usuario.CLIENTE:
        form_class = RegistroClienteForm
    else:
        form_class = RegistroAdminForm
    
    if request.method == 'POST':
        form = form_class(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('administrar_usuarios')
    else:
        form = form_class(instance=usuario)
    
    return render(request, 'panel_admin/gestion_usuarios/form_usuario.html', {
        'form': form,
        'titulo': f'Editar {usuario.get_tipo_usuario_display()}',
        'accion': 'Actualizar',
        'usuario': usuario,
    })

@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    """Vista para eliminar un usuario."""
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        tipo = usuario.get_tipo_usuario_display()
        usuario.delete()
        messages.success(request, f'{tipo} eliminado exitosamente.')
        return redirect('administrar_usuarios')
    
    return render(request, 'panel_admin/gestion_usuarios/confirmar_eliminar.html', {
        'usuario': usuario,
    })



@login_required
@user_passes_test(es_admin)
def administrar_inversiones(request):
    """Vista para listar y gestionar tipos de inversión."""
    inversiones = TipoInversion.objects.all()
    inversiones_bajo = TipoInversion.objects.filter(riesgo='BAJO')
    inversiones_medio = TipoInversion.objects.filter(riesgo='MEDIO')
    inversiones_alto = TipoInversion.objects.filter(riesgo='ALTO')
    
    return render(request, 'panel_admin/gestor_inversiones.html', {
        'inversiones': inversiones,
        'inversiones_bajo': inversiones_bajo,
        'inversiones_medio': inversiones_medio,
        'inversiones_alto': inversiones_alto,
    })

@login_required
@user_passes_test(es_admin)
def detalle_tipo_inversion(request, inversion_id):
    """Vista para ver detalles de un tipo de inversión específico."""
    inversion = get_object_or_404(TipoInversion, id=inversion_id)
    return render(request, 'panel_admin/gestion_inversiones/detalle_inversion.html', {
        'inversion': inversion,
    })

@login_required
@user_passes_test(es_admin)
def crear_tipo_inversion(request):
    """Vista para crear un nuevo tipo de inversión."""
    if request.method == 'POST':
        form = TipoInversionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de inversión creado exitosamente.')
            return redirect('administrar_inversiones')
    else:
        form = TipoInversionForm()
    
    return render(request, 'panel_admin/gestion_inversiones/form_inversion.html', {
        'form': form,
        'titulo': 'Nuevo Tipo de Inversión',
        'accion': 'Crear',
    })

@login_required
@user_passes_test(es_admin)
def editar_tipo_inversion(request, inversion_id):
    """Vista para editar un tipo de inversión existente."""
    inversion = get_object_or_404(TipoInversion, id=inversion_id)
    
    if request.method == 'POST':
        form = TipoInversionForm(request.POST, instance=inversion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de inversión actualizado exitosamente.')
            return redirect('administrar_inversiones')
    else:
        form = TipoInversionForm(instance=inversion)
    
    return render(request, 'panel_admin/gestion_inversiones/form_inversion.html', {
        'form': form,
        'titulo': f'Editar Tipo de Inversión',
        'accion': 'Actualizar',
        'inversion': inversion,
    })

@login_required
@user_passes_test(es_admin)
def eliminar_tipo_inversion(request, inversion_id):
    """Vista para eliminar un tipo de inversión."""
    inversion = get_object_or_404(TipoInversion, id=inversion_id)
    
    if request.method == 'POST':
        nombre = inversion.nombre
        inversion.delete()
        messages.success(request, f'Tipo de inversión "{nombre}" eliminado exitosamente.')
        return redirect('administrar_inversiones')
    
    return render(request, 'panel_admin/gestion_inversiones/confirmar_eliminar.html', {
        'inversion': inversion,
    })



@login_required
@user_passes_test(es_admin)
def administrar_creditos(request):
    """Vista para listar y gestionar tipos de crédito."""
    tipos_credito = TipoCredito.objects.all()
    
    # Podemos organizarlos por rangos de tasas de interés (como ejemplo)
    creditos_bajo_interes = TipoCredito.objects.filter(tasa_interes_referencial__lte=6)
    creditos_medio_interes = TipoCredito.objects.filter(tasa_interes_referencial__gt=6, tasa_interes_referencial__lte=9)
    creditos_alto_interes = TipoCredito.objects.filter(tasa_interes_referencial__gt=9)
   
    return render(request, 'panel_admin/gestor_creditos.html', {
        'tipos_credito': tipos_credito,
        'creditos_bajo_interes': creditos_bajo_interes,
        'creditos_medio_interes': creditos_medio_interes,
        'creditos_alto_interes': creditos_alto_interes,
    })

@login_required
@user_passes_test(es_admin)
def detalle_tipo_credito(request, credito_id):
    """Vista para ver detalles de un tipo de crédito específico."""
    tipo_credito = get_object_or_404(TipoCredito, id=credito_id)
    return render(request, 'panel_admin/gestion_creditos/detalle_credito.html', {
        'tipo_credito': tipo_credito,
    })

@login_required
@user_passes_test(es_admin)
def crear_tipo_credito(request):
    """Vista para crear un nuevo tipo de crédito."""
    if request.method == 'POST':
        form = TipoCreditoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de crédito creado exitosamente.')
            return redirect('administrar_creditos')
    else:
        form = TipoCreditoForm()
   
    return render(request, 'panel_admin/gestion_creditos/form_credito.html', {
        'form': form,
        'titulo': 'Nuevo Tipo de Crédito',
        'accion': 'Crear',
    })

@login_required
@user_passes_test(es_admin)
def editar_tipo_credito(request, credito_id):
    """Vista para editar un tipo de crédito existente."""
    tipo_credito = get_object_or_404(TipoCredito, id=credito_id)
   
    if request.method == 'POST':
        form = TipoCreditoForm(request.POST, instance=tipo_credito)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de crédito actualizado exitosamente.')
            return redirect('administrar_creditos')
    else:
        form = TipoCreditoForm(instance=tipo_credito)
   
    return render(request, 'panel_admin/gestion_creditos/form_credito.html', {
        'form': form,
        'titulo': f'Editar Tipo de Crédito',
        'accion': 'Actualizar',
        'tipo_credito': tipo_credito,
    })

@login_required
@user_passes_test(es_admin)
def eliminar_tipo_credito(request, credito_id):
    """Vista para eliminar un tipo de crédito."""
    tipo_credito = get_object_or_404(TipoCredito, id=credito_id)
   
    if request.method == 'POST':
        nombre = tipo_credito.nombre
        tipo_credito.delete()
        messages.success(request, f'Tipo de crédito "{nombre}" eliminado exitosamente.')
        return redirect('administrar_creditos')
   
    return render(request, 'panel_admin/gestion_creditos/confirmar_eliminar.html', {
        'tipo_credito': tipo_credito,
    })


@login_required
@user_passes_test(es_admin)
def administrar_reportes(request):
    """Vista para listar y gestionar reportes de simulaciones."""
    # Obtener todos los reportes
    inversiones = Inversion.objects.all().order_by('-fecha_creacion')
    creditos = Credito.objects.all().order_by('-fecha_creacion')
    
    # Filtro por tipo de reporte
    tipo_reporte = request.GET.get('tipo', 'todos')
    
    if tipo_reporte == 'inversiones':
        creditos = []
    elif tipo_reporte == 'creditos':
        inversiones = []
    
    return render(request, 'panel_admin/gestor_reportes.html', {
        'inversiones': inversiones,
        'creditos': creditos,
        'tipo_activo': tipo_reporte,
    })

@login_required
@user_passes_test(es_admin)
def detalle_reporte_inversion(request, inversion_id):
    """Vista para ver detalles de un reporte de inversión específico."""
    inversion = get_object_or_404(Inversion, id=inversion_id)
    ganancia = inversion.capital_final - inversion.monto_invertido  # cálculo directo en Python
    return render(request, 'panel_admin/gestion_reportes/detalle_inversion.html', {
        'inversion': inversion,
        'ganancia': ganancia,  # pasamos el valor al template
    })

@login_required
@user_passes_test(es_admin)
def detalle_reporte_credito(request, credito_id):
    """Vista para ver detalles de un reporte de crédito específico."""
    credito = get_object_or_404(Credito, id=credito_id)
    return render(request, 'panel_admin/gestion_reportes/detalle_credito.html', {
        'credito': credito,
    })

