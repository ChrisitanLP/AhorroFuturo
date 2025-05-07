from django import forms
from .models import ConfiguracionGlobal

class ConfiguracionGeneralForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = '__all__'
        widgets = {
            'nombre_sitio': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_corta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_atencion': forms.TextInput(attrs={'class': 'form-control'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_soporte': forms.EmailInput(attrs={'class': 'form-control'}),
            'horario_atencion': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_emergencias': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
            'texto_copyright': forms.TextInput(attrs={'class': 'form-control'}),
            'texto_legal': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LogoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['logo']
        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control d-none', 'accept': 'image/*'})
        }

class FaviconForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['favicon']
        widgets = {
            'favicon': forms.FileInput(attrs={'class': 'form-control d-none', 'accept': 'image/*'})
        }

class InfoSitioForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['nombre_sitio', 'descripcion_corta']
        widgets = {
            'nombre_sitio': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_corta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class InfoContactoForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['direccion', 'telefono_principal', 'telefono_atencion', 
                  'email_contacto', 'email_soporte', 'horario_atencion', 'horario_emergencias']
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_atencion': forms.TextInput(attrs={'class': 'form-control'}),
            'email_contacto': forms.EmailInput(attrs={'class': 'form-control'}),
            'email_soporte': forms.EmailInput(attrs={'class': 'form-control'}),
            'horario_atencion': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_emergencias': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RedesSocialesForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['facebook', 'twitter', 'linkedin', 'instagram']
        widgets = {
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://twitter.com/...'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
        }

class InformacionLegalForm(forms.ModelForm):
    class Meta:
        model = ConfiguracionGlobal
        fields = ['texto_copyright', 'texto_legal']
        widgets = {
            'texto_copyright': forms.TextInput(attrs={'class': 'form-control'}),
            'texto_legal': forms.TextInput(attrs={'class': 'form-control'}),
        }