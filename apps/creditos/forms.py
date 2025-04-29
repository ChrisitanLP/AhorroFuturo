# forms.py
from django import forms
from .models import TipoCredito, Credito

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