from django import forms
from .models import TipoInversion

class SimuladorInversionForm(forms.Form):
    tipo_inversion = forms.ModelChoiceField(
        queryset=TipoInversion.objects.filter(es_activo=True),
        empty_label="Seleccione tipo de inversión",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
    
    monto_inversion = forms.DecimalField(
        min_value=0.01,
        max_digits=10,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control numero-formato',
            'placeholder': 'Ej: $5000'
        })
    )
    
    plazo = forms.IntegerField(
        min_value=1,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control form-select'})
    )
    
    reinversion_intereses = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class TipoInversionForm(forms.ModelForm):
    """Formulario para la creación y edición de tipos de inversión."""
    
    class Meta:
        model = TipoInversion
        fields = [
            'nombre',
            'descripcion',
            'rentabilidad_anual_minima',
            'rentabilidad_anual_maxima',
            'plazo_minimo',
            'plazo_maximo',
            'monto_minimo',
            'monto_maximo',
            'riesgo',
            'es_activo',
        ]
        
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }
        
    def clean(self):
        """Validaciones personalizadas para el formulario."""
        cleaned_data = super().clean()
        
        # Validar que rentabilidad máxima > rentabilidad mínima
        rent_min = cleaned_data.get('rentabilidad_anual_minima')
        rent_max = cleaned_data.get('rentabilidad_anual_maxima')
        if rent_min is not None and rent_max is not None and rent_max <= rent_min:
            self.add_error('rentabilidad_anual_maxima', 
                          'La rentabilidad máxima debe ser mayor que la rentabilidad mínima.')
        
        # Validar que plazo máximo > plazo mínimo
        plazo_min = cleaned_data.get('plazo_minimo')
        plazo_max = cleaned_data.get('plazo_maximo')
        if plazo_min is not None and plazo_max is not None and plazo_max <= plazo_min:
            self.add_error('plazo_maximo', 
                          'El plazo máximo debe ser mayor que el plazo mínimo.')
        
        # Validar que monto máximo > monto mínimo
        monto_min = cleaned_data.get('monto_minimo')
        monto_max = cleaned_data.get('monto_maximo')
        if monto_min is not None and monto_max is not None and monto_max <= monto_min:
            self.add_error('monto_maximo', 
                          'El monto máximo debe ser mayor que el monto mínimo.')
        
        return cleaned_data