from django.contrib import admin
from .models import TipoCredito, Credito

@admin.register(TipoCredito)
class TipoCreditoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tasa_interes_referencial', 'plazo_minimo', 'plazo_maximo', 'monto_minimo', 'monto_maximo')
    search_fields = ('nombre',)

@admin.register(Credito)
class CreditoAdmin(admin.ModelAdmin):
    list_display = ('tipo_credito', 'usuario', 'monto_prestamo', 'plazo', 'metodo_pago', 'fecha_creacion')
    list_filter = ('tipo_credito', 'metodo_pago')
    search_fields = ('usuario__username', 'usuario__email')
    date_hierarchy = 'fecha_creacion'