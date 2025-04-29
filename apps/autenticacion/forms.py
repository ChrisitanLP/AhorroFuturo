from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombre de usuario'}),
        label='Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Contraseña'}),
        label='Contraseña'
    )

class RegistroClienteForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Email'}),
        required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Nombres'}),
        label='Nombres'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Apellidos'}),
        label='Apellidos'
    )
    telefono = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Teléfono'}),
        required=False,
        label='Teléfono'
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'telefono', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuario',
            'data-bs-toggle': 'tooltip',
            'title': '150 caracteres o menos. Solo letras, números y @/./+/-/_'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'label': 'Contraseña',
            'data-bs-toggle': 'tooltip',
            'title': 'La contraseña debe tener al menos 8 caracteres, no ser completamente numérica ni similar a tus datos personales.'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'label': 'Confirmar Contraseña',
            'data-bs-toggle': 'tooltip',
            'title': 'Ingresa la misma contraseña para confirmarla.'
        })
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = Usuario.CLIENTE
        if commit:
            user.save()
        return user

class RegistroAdminForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Nombres'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Apellidos'
    )
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Usuario',
            'title': '150 caracteres o menos. Solo letras, números y @/./+/-/_'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'title': 'La contraseña debe tener al menos 8 caracteres, no ser completamente numérica ni similar a tus datos personales.'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña',
            'title': 'Ingresa la misma contraseña para confirmarla.'
        })
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.tipo_usuario = Usuario.ADMIN
        if commit:
            user.save()
        return user