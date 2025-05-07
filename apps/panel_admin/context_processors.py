from .models import ConfiguracionGlobal

def logo_context(request):
    config = ConfiguracionGlobal.objects.first()
    return {'logo': config.logo.url if config and config.logo else None}
