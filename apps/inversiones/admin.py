from django.contrib import admin
from .models import TipoInversion, PlazoInversion, Inversion

class PlazoInversionInline(admin.TabularInline):
    model = PlazoInversion
    extra = 1

@admin.register(TipoInversion)
class TipoInversionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tasa_rendimiento', 'plazo_minimo', 'plazo_maximo', 'monto_minimo', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    inlines = [PlazoInversionInline]

@admin.register(Inversion)
class InversionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_inversion', 'monto', 'plazo', 'tasa_rendimiento', 'fecha_simulacion')
    list_filter = ('tipo_inversion', 'fecha_simulacion')
    search_fields = ('usuario__username', 'tipo_inversion__nombre')