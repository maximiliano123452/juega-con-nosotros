from django import forms
from django.contrib.auth.hashers import make_password, check_password
from .models import Usuario
from django.conf import settings
from django.forms import DateInput


# Formulario de registro de usuario
class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control'}),
        label="Contraseña"
    )
    repetir_contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña', 'class': 'form-control'}),
        label="Repetir Contraseña"
    )
    terminos = forms.BooleanField(
        label="Acepto los términos y condiciones",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    fecha_nacimiento = forms.DateField(
        required=False,
        widget=DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=['%Y-%m-%d']
    )
    class Meta:
        model = Usuario
        fields = [
            'nombre_completo',
            'nombre_usuario',
            'correo_electronico',
            'contrasena',
            'fecha_nacimiento',
            'direccion_despacho',
            'rol',
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa Nombres y Apellidos'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu Nombre de Usuario'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'}),
            'direccion_despacho': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe tu dirección (Opcional)'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("contrasena")
        password2 = cleaned_data.get("repetir_contrasena")

        if password and password2 and password != password2:
            self.add_error('repetir_contrasena', "Las contraseñas no coinciden")

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.contrasena = make_password(self.cleaned_data['contrasena'])  # Hasheamos la contraseña
        if commit:
            usuario.save()
        return usuario



# Formulario de inicio de sesión

class LoginForm(forms.Form):
    correo_electronico = forms.EmailField(
        label="Correo Electrónico", 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'})
    )
    contrasena = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
    )



# Formulario de actualización de perfil de usuario
class PerfilForm(forms.ModelForm):
    contrasena = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva Contraseña', 'class': 'form-control'}),
        label="Nueva Contraseña"
    )
    repetir_contrasena = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña', 'class': 'form-control'}),
        label="Repetir Contraseña"
    )
    direccion_despacho = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nueva Dirección (Opcional)', 'class': 'form-control'}),
        label="Dirección"
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre_completo',
            'nombre_usuario',
            'correo_electronico',
            'fecha_nacimiento',
            'direccion_despacho'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre completo'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre de usuario'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo Electrónico'}),
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d',
                                                attrs={'type': 'date', 'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("contrasena")
        password2 = cleaned_data.get("repetir_contrasena")

        if password and password2 and password != password2:
            self.add_error('repetir_contrasena', "Las contraseñas no coinciden")

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('contrasena')

        if password:
            usuario.contrasena = make_password(password)

        if commit:
            usuario.save()
        return usuario