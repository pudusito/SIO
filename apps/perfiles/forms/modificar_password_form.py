import string
from django import forms


letras_minusculas = string.ascii_lowercase + 'ñ'
letras_mayusculas = string.ascii_uppercase + 'Ñ'
numeros = string.digits
especiales = string.punctuation



class ModificarPasswordForm(forms.Form):
    new_password = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput(
        attrs={'id':'new-password', 'placeholder': '••••••••'}
    ), label="Nueva Contraseña", required=True)

    confirm_password = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput(
        attrs={'id':'confirm-password', 'placeholder': '••••••••'}
    ), label='Confirmar Nueva Contraseña' , required=True)



    # Aqui valido que la contraseña respete las validaciones
    def clean(self):
        # Aqui hacemos que Form aplique las validaciones estandar o default de 
        # los CharField, como las longitudes
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        errores = []

        if new_password != confirm_password:
            errores.append('Las contraseñas no coinciden. Deben ser Identicas')
        
        for letra in letras_minusculas:
            if letra in new_password:
                break
        else:
            errores.append('La contraseña debe contener al menos una letra en minusculas')

        for letra in letras_mayusculas:
            if letra in new_password:
                break
        else:
            errores.append('La contraseña debe contener al menos una letra en mayusculas')

        for caracter in especiales:
            if caracter in new_password:
                break
        else:
            errores.append(f'La contraseña debe contener al menos un caracter de estos: {especiales}')
        
        for numero in numeros:
            if numero in new_password:
                break
        else:
            errores.append('La contraseña debe contener al menos un numero')

        if errores:
            raise forms.ValidationError(errores)

        return cleaned_data