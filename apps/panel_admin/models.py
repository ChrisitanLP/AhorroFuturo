from django.db import models

class ConfiguracionGlobal(models.Model):
    nombre = models.CharField(max_length=100, default="Configuración General")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nombre