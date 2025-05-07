from .models import ConfiguracionGlobal

def configuracion_global(request):
    """
    Agrega la configuración global al contexto de todas las plantillas
    """
    try:
        config = ConfiguracionGlobal.objects.first()
        if not config:
            config = ConfiguracionGlobal.objects.create()
        
        return {
            'config': config,
            'logo': config.logo.url if config.logo else None,
            'favicon': config.favicon.url if config.favicon else None
        }
    except Exception:
        # En caso de error (como durante migraciones), devolver valores predeterminados
        return {
            'config': None,
            'logo': None,
            'favicon': None
        }