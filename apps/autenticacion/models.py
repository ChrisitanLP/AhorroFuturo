from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    ADMIN = 'admin'
    CLIENTE = 'cliente'
    
    TIPOS_USUARIO = [
        (ADMIN, 'Administrador'),
        (CLIENTE, 'Cliente'),
    ]
    
    tipo_usuario = models.CharField(max_length=10, choices=TIPOS_USUARIO, default=CLIENTE)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    
    def es_admin(self):
        return self.tipo_usuario == self.ADMIN
    
    def es_cliente(self):
        return self.tipo_usuario == self.CLIENTE