from django import forms
from .models import TipoCredito, Credito
import json

class SimuladorForm(forms.Form):
    tipo_credito = forms.ModelChoiceField(queryset=TipoCredito.objects.all())
    monto_vivienda = forms.DecimalField(max_digits=12, decimal_places=2)
    monto_prestamo = forms.DecimalField(max_digits=12, decimal_places=2)
    plazo = forms.IntegerField(min_value=1)
    metodo_pago = forms.ChoiceField(choices=Credito.METODO_CHOICES)
    
    def clean(self):
        cleaned_data = super().clean()
        tipo_credito = cleaned_data.get('tipo_credito')
        monto_prestamo = cleaned_data.get('monto_prestamo')
        plazo = cleaned_data.get('plazo')
        
        if tipo_credito and monto_prestamo:
            if monto_prestamo < tipo_credito.monto_minimo:
                self.add_error('monto_prestamo', f'El monto mínimo es {tipo_credito.monto_minimo}')
            if monto_prestamo > tipo_credito.monto_maximo:
                self.add_error('monto_prestamo', f'El monto máximo es {tipo_credito.monto_maximo}')
                
        if tipo_credito and plazo:
            if plazo < tipo_credito.plazo_minimo:
                self.add_error('plazo', f'El plazo mínimo es {tipo_credito.plazo_minimo} meses')
            if plazo > tipo_credito.plazo_maximo:
                self.add_error('plazo', f'El plazo máximo es {tipo_credito.plazo_maximo} meses')
                
        return cleaned_data

class TipoCreditoForm(forms.ModelForm):
    """Formulario para crear y editar tipos de crédito."""
    
    # Campos para los seguros
    seguro_desgravamen = forms.DecimalField(
        label="Seguro de Desgravamen (%)",
        max_digits=5,
        decimal_places=2,
        required=False,
        help_text="Porcentaje del seguro de desgravamen"
    )
    
    seguro_incendio = forms.DecimalField(
        label="Seguro de Incendio (%)",
        max_digits=5,
        decimal_places=2,
        required=False,
        help_text="Porcentaje del seguro de incendio"
    )
    
    seguro_bien = forms.DecimalField(
        label="Seguro del Bien (%)",
        max_digits=5,
        decimal_places=2,
        required=False,
        help_text="Porcentaje del seguro del bien"
    )
    
    seguro_vehicular = forms.DecimalField(
        label="Seguro Vehicular (%)",
        max_digits=5,
        decimal_places=2,
        required=False,
        help_text="Porcentaje del seguro vehicular"
    )
    
    class Meta:
        model = TipoCredito
        fields = [
            'nombre', 
            'tasa_interes_referencial', 
            'tasa_interes_minima', 
            'tasa_interes_maxima', 
            'plazo_minimo', 
            'plazo_maximo', 
            'monto_minimo', 
            'monto_maximo'
        ]
        labels = {
            'nombre': 'Nombre del Tipo de Crédito',
            'tasa_interes_referencial': 'Tasa de Interés Referencial (%)',
            'tasa_interes_minima': 'Tasa de Interés Mínima (%)',
            'tasa_interes_maxima': 'Tasa de Interés Máxima (%)',
            'plazo_minimo': 'Plazo Mínimo (meses)',
            'plazo_maximo': 'Plazo Máximo (meses)',
            'monto_minimo': 'Monto Mínimo ($)',
            'monto_maximo': 'Monto Máximo ($)',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tasa_interes_referencial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_minima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tasa_interes_maxima': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'plazo_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
            'plazo_maximo': forms.NumberInput(attrs={'class': 'form-control'}),
            'monto_minimo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monto_maximo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando un objeto existente, cargamos los valores de los seguros
        if self.instance.pk:
            seguros = self.instance.get_seguros()
            self.fields['seguro_desgravamen'].initial = seguros.get('desgravamen', 0)
            self.fields['seguro_incendio'].initial = seguros.get('incendio', 0)
            self.fields['seguro_bien'].initial = seguros.get('bien', 0)
            self.fields['seguro_vehicular'].initial = seguros.get('vehicular', 0)
    
    def clean(self):
        """Validación personalizada para asegurar que los valores mínimos y máximos sean consistentes."""
        cleaned_data = super().clean()
        
        # Validar que la tasa mínima sea menor o igual que la máxima
        tasa_min = cleaned_data.get('tasa_interes_minima')
        tasa_max = cleaned_data.get('tasa_interes_maxima')
        if tasa_min and tasa_max and tasa_min > tasa_max:
            self.add_error('tasa_interes_minima', 'La tasa mínima no puede ser mayor que la máxima')
        
        # Validar que el plazo mínimo sea menor o igual que el máximo
        plazo_min = cleaned_data.get('plazo_minimo')
        plazo_max = cleaned_data.get('plazo_maximo')
        if plazo_min and plazo_max and plazo_min > plazo_max:
            self.add_error('plazo_minimo', 'El plazo mínimo no puede ser mayor que el máximo')
        
        # Validar que el monto mínimo sea menor o igual que el máximo
        monto_min = cleaned_data.get('monto_minimo')
        monto_max = cleaned_data.get('monto_maximo')
        if monto_min and monto_max and monto_min > monto_max:
            self.add_error('monto_minimo', 'El monto mínimo no puede ser mayor que el máximo')
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guarda el formulario con los campos de seguros procesados."""
        instance = super().save(commit=False)
        
        # Construir el diccionario de seguros
        seguros = {}
        
        if self.cleaned_data.get('seguro_desgravamen'):
            seguros['desgravamen'] = float(self.cleaned_data.get('seguro_desgravamen'))
        
        if self.cleaned_data.get('seguro_incendio'):
            seguros['incendio'] = float(self.cleaned_data.get('seguro_incendio'))
        
        if self.cleaned_data.get('seguro_bien'):
            seguros['bien'] = float(self.cleaned_data.get('seguro_bien'))
        
        if self.cleaned_data.get('seguro_vehicular'):
            seguros['vehicular'] = float(self.cleaned_data.get('seguro_vehicular'))
        
        # Asignar el diccionario de seguros
        instance.seguros = seguros
        
        if commit:
            instance.save()
        
        return instance