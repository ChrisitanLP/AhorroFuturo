from django.db import models
from django.utils import timezone

class Institucion(models.Model):
    nombre = models.CharField(max_length=100)
    slogan = models.CharField(max_length=200, blank=True, null=True)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    sitio_web = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='institucion/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Institución"
        verbose_name_plural = "Institución"

class ContactoMensaje(models.Model):
    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    asunto = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(default=timezone.now)
    leido = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.asunto} - {self.nombre}"
    
    class Meta:
        verbose_name = "Mensaje de contacto"
        verbose_name_plural = "Mensajes de contacto"
        ordering = ['-fecha_creacion']