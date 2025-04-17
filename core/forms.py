from django import forms 
from django.contrib.auth.hashers import make_password
from .models import Usuario, Juego
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
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
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
        usuario.contrasena = make_password(self.cleaned_data['contrasena'])
        if commit:
            usuario.save()
        return usuario


# Formulario de inicio de sesion
class LoginForm(forms.Form):
    correo_electronico = forms.EmailField(
        label="Correo Electrónico", 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tucorreo@ejemplo.com'})
    )
    contrasena = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu contraseña'})
    )


# Formulario de actualizacion de perfil de usuario
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

    correo_electronico = forms.EmailField(
        label="Correo (No se puede modificar)",
        required=False,
        disabled=True,
        widget=forms.EmailInput(attrs={'class': 'form-control correo-modificar', 'placeholder': 'Ingresa tu correo electrónico'})
    )

    class Meta:
        model = Usuario
        fields = [
            'nombre_completo',
            'nombre_usuario',
            'correo_electronico',
            'fecha_nacimiento',
            'direccion_despacho',
            'rol'
        ]
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre completo'}),
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingresa tu nombre de usuario'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'fecha_nacimiento': forms.DateInput(format='%Y-%m-%d',
                                                attrs={'type': 'date', 'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'})
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


# Formulario para agregar juegos
class JuegoForm(forms.ModelForm):
    class Meta:
        model = Juego
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'plataformas', 'imagen']  # Incluir todos los campos del modelo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del juego'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Precio'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'plataformas': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
