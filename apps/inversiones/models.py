from django.db import models
from django.conf import settings

class TipoInversion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tasa_rendimiento = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tasa anual")
    plazo_minimo = models.IntegerField(help_text="Plazo mínimo en meses")
    plazo_maximo = models.IntegerField(help_text="Plazo máximo en meses")
    monto_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} - {self.tasa_rendimiento}%"
    
    class Meta:
        verbose_name = "Tipo de Inversión"
        verbose_name_plural = "Tipos de Inversión"

class PlazoInversion(models.Model):
    tipo_inversion = models.ForeignKey(TipoInversion, on_delete=models.CASCADE, related_name='plazos')
    plazo_meses = models.IntegerField()
    tasa_rendimiento = models.DecimalField(max_digits=5, decimal_places=2, help_text="Tasa específica para este plazo")
    
    def __str__(self):
        return f"{self.tipo_inversion.nombre} - {self.plazo_meses} meses - {self.tasa_rendimiento}%"
    
    class Meta:
        verbose_name = "Plazo de Inversión"
        verbose_name_plural = "Plazos de Inversión"
        unique_together = ['tipo_inversion', 'plazo_meses']

class Inversion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_inversion = models.ForeignKey(TipoInversion, on_delete=models.PROTECT)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    plazo = models.IntegerField(help_text="Plazo en meses")
    tasa_rendimiento = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_simulacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Inversión {self.tipo_inversion.nombre} - ${self.monto} - {self.plazo} meses"
    
    class Meta:
        verbose_name = "Inversión"
        verbose_name_plural = "Inversiones"