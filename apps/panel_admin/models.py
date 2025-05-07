from django.db import models

class ConfiguracionGlobal(models.Model):
    # Información general
    nombre_sitio = models.CharField(max_length=100, default="Ahorro Futuro")
    descripcion_corta = models.CharField(max_length=255, default="Somos una institución financiera comprometida con tu desarrollo económico y bienestar financiero.")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    favicon = models.ImageField(upload_to='logos/', null=True, blank=True)
    
    # Información de contacto
    direccion = models.CharField(max_length=255, default="Av. Principal 123, Ciudad")
    telefono_principal = models.CharField(max_length=50, default="(01) 123-4567")
    telefono_atencion = models.CharField(max_length=50, default="800 123 4567")
    email_contacto = models.EmailField(default="contacto@ahorrofuturo.com")
    email_soporte = models.EmailField(default="soporte@ahorrofuturo.com")
    horario_atencion = models.CharField(max_length=100, default="Lun-Vie: 9:00 - 17:00")
    horario_emergencias = models.CharField(max_length=100, default="24/7 para emergencias")
    
    # Redes sociales
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    
    # Información legal
    texto_copyright = models.CharField(max_length=255, default="Todos los derechos reservados.")
    texto_legal = models.CharField(max_length=255, default="Supervisado por la Superintendencia de Banca y Seguros.")

    def __str__(self):
        return self.nombre_sitio
    
class ConfiguracionLogo(models.Model):
    nombre = models.CharField(max_length=100, default="Configuración General")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return self.nombre