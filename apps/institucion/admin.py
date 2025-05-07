from django.contrib import admin
from .models import Institucion, ContactoMensaje

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')

@admin.register(ContactoMensaje)
class ContactoMensajeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'asunto', 'fecha_creacion', 'leido')
    list_filter = ('leido', 'fecha_creacion', 'asunto')
    search_fields = ('nombre', 'correo', 'mensaje')
    date_hierarchy = 'fecha_creacion'
    
    def mark_as_read(self, request, queryset):
        queryset.update(leido=True)
    mark_as_read.short_description = "Marcar como leído"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(leido=False)
    mark_as_unread.short_description = "Marcar como no leído"
    
    actions = ['mark_as_read', 'mark_as_unread']