from django.contrib import admin
from .models import TipoInversion, PerfilRiesgo

class TipoInversionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'riesgo', 'rentabilidad_anual_minima', 
                    'rentabilidad_anual_maxima', 'monto_minimo', 
                    'monto_maximo', 'plazo_minimo', 'plazo_maximo', 'es_activo')
    list_filter = ('riesgo', 'es_activo')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('es_activo',)
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'riesgo', 'es_activo')
        }),
        ('Rentabilidad', {
            'fields': ('rentabilidad_anual_minima', 'rentabilidad_anual_maxima')
        }),
        ('Plazos permitidos', {
            'fields': ('plazo_minimo', 'plazo_maximo')
        }),
        ('Montos permitidos', {
            'fields': ('monto_minimo', 'monto_maximo')
        }),
    )

class PerfilRiesgoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nivel_riesgo', 'get_tipos_inversion')
    list_filter = ('nivel_riesgo',)
    search_fields = ('nombre', 'descripcion')
    filter_horizontal = ('tipos_inversion_recomendados',)
    
    def get_tipos_inversion(self, obj):
        return ", ".join([tipo.nombre for tipo in obj.tipos_inversion_recomendados.all()[:3]])
    
    get_tipos_inversion.short_description = "Tipos de inversión recomendados"

# Registrar los modelos con sus clases de administración personalizadas
admin.site.register(TipoInversion, TipoInversionAdmin)
admin.site.register(PerfilRiesgo, PerfilRiesgoAdmin)