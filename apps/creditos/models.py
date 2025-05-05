from django.db import models
from django.conf import settings # Importa settings en lugar de User directamente
import json

class TipoCredito(models.Model):
    nombre = models.CharField(max_length=100)
    tasa_interes_referencial = models.DecimalField(max_digits=5, decimal_places=2)
    tasa_interes_minima = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tasa_interes_maxima = models.DecimalField(max_digits=5, decimal_places=2, default=12.00)
    plazo_minimo = models.IntegerField(help_text="Plazo mínimo en meses")
    plazo_maximo = models.IntegerField(help_text="Plazo máximo en meses")
    monto_minimo = models.DecimalField(max_digits=12, decimal_places=2)
    monto_maximo = models.DecimalField(max_digits=12, decimal_places=2)

    # Campo JSON para almacenar múltiples tipos de seguros
    seguros = models.JSONField(default=dict, help_text="Tasas de seguros en formato JSON")
    
    # Campos legacy para compatibilidad con código existente
    tasa_seguro_desgravamen = models.DecimalField(max_digits=5, decimal_places=3, default=0.03, 
                                               help_text="Tasa mensual de seguro de desgravamen (porcentaje)")
    tasa_seguro_bien = models.DecimalField(max_digits=5, decimal_places=3, default=0.00, 
                                        help_text="Tasa mensual de seguro del bien (porcentaje)")
    
    def save(self, *args, **kwargs):
        # Asegurar que los campos legacy estén sincronizados con el campo JSON
        if self.seguros:
            seguros_dict = self.seguros if isinstance(self.seguros, dict) else json.loads(self.seguros)
            if 'desgravamen' in seguros_dict:
                self.tasa_seguro_desgravamen = seguros_dict['desgravamen'] / 100  # Convertir de porcentaje a decimal
            if 'bien' in seguros_dict:
                self.tasa_seguro_bien = seguros_dict['bien'] / 100  # Convertir de porcentaje a decimal
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre

    def get_seguros(self):
        """Obtiene todos los seguros como un diccionario"""
        if isinstance(self.seguros, str):
            return json.loads(self.seguros)
        return self.seguros or {}

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