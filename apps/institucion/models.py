from django.db import models

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