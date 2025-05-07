from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMIN = 'administrador'
    CLIENTE = 'cliente'
    
    TIPOS_USUARIO = [
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
    ]
    
    telefono = models.CharField(max_length=10, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=15, choices=TIPOS_USUARIO, default=CLIENTE)

    def es_admin(self):
        return self.is_superuser
    
    def es_cliente(self):
        return not self.is_superuser
