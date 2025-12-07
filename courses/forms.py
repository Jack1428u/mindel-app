from django import forms
from django.contrib.auth.models import User

class UserForm(forms.Form):
    username = forms.CharField(max_length=16)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El username ya existe, ingrese otro por favor.")
        if(len(username) < 2):
            raise forms.ValidationError("\nDebe tener minimo 2 caracteres")
        if not username.isalpha():
            raise forms.ValidationError("\nDebe contener solo letras")
        return username
    def clean_email(self):
        # Obtener email del formulario(entrada del usuarios), no de la BD
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("\nEl email ya existe")
        if len(email) < 4:
            raise forms.ValidationError("El email no es valido")
        return email
    def clean_password(self):
        password = self.cleaned_data.get('password').strip()
        if len(password) < 8:
            raise forms.ValidationError("\nLa contrasena debe tener minimo 8 caracteres")
        if not password:
            raise forms.ValidationError("\nLa contraseña es obligatoria")
        return password
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password').strip()
        confirm_password = self.cleaned_data.get('password_confirm').strip()
        if password != confirm_password:
            raise forms.ValidationError("\nLa contraseña debe coincidir.")
        return confirm_password