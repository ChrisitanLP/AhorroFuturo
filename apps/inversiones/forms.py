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