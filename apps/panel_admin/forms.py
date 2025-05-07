from django import forms
from .models import ConfiguracionGlobal

class LogoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['logo']
