from django.contrib import admin
from .models import Institucion

@admin.register(Institucion)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email')