from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TipoInversion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    rentabilidad_anual_minima = models.DecimalField(max_digits=5, decimal_places=2)
    rentabilidad_anual_maxima = models.DecimalField(max_digits=5, decimal_places=2)
    plazo_minimo = models.IntegerField(help_text="Plazo mínimo en meses")
    plazo_maximo = models.IntegerField(help_text="Plazo máximo en meses")
    monto_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    monto_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    riesgo = models.CharField(max_length=20, choices=[
        ('BAJO', 'Bajo'),
        ('MEDIO', 'Medio'),
        ('ALTO', 'Alto')
    ])
    es_activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Tipo de Inversión"
        verbose_name_plural = "Tipos de Inversión"


class PerfilRiesgo(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    nivel_riesgo = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    tipos_inversion_recomendados = models.ManyToManyField(TipoInversion, related_name="perfiles_riesgo")
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Perfil de riesgo"
        verbose_name_plural = "Perfiles de riesgo"