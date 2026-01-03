from django.contrib.auth.forms import AuthenticationForm
from django import forms

# Formulario para autenticar pero configurado para usar el Email como identificador
# para validar la identidad del usuario
class LoginEmailForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(
    attrs={'placeholder': "Tu Correo Institucional"}
    ))


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = "••••••••"
        self.fields['username'].label = "Email"



class CodigoVerificacionEmailForm(forms.Form):
    codigo = forms.IntegerField(min_value=100_000, max_value=999_999, widget=forms.HiddenInput(attrs={'id':'otp-hidden'}))