from django.db import models
from django.conf import settings  # Importa settings en lugar de User directamente

class TipoCredito(models.Model):
    nombre = models.CharField(max_length=100)
    tasa_interes_referencial = models.DecimalField(max_digits=5, decimal_places=2)
    plazo_minimo = models.IntegerField(help_text="Plazo mínimo en meses")
    plazo_maximo = models.IntegerField(help_text="Plazo máximo en meses")
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2)
    monto_maximo = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self):
        return self.nombre

class Credito(models.Model):
    METODO_CHOICES = [
        ('frances', 'Método Francés'),
        ('aleman', 'Método Alemán'),
    ]
    
    # Reemplaza User directo por settings.AUTH_USER_MODEL
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    tipo_credito = models.ForeignKey(TipoCredito, on_delete=models.CASCADE)
    monto_vivienda = models.DecimalField(max_digits=12, decimal_places=2)
    monto_prestamo = models.DecimalField(max_digits=12, decimal_places=2)
    plazo = models.IntegerField(help_text="Plazo en meses")
    metodo_pago = models.CharField(max_length=10, choices=METODO_CHOICES, default="frances")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Crédito {self.tipo_credito.nombre} - {self.monto_prestamo}"